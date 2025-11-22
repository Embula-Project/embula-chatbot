from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from src.config import settings
from src.config.prompts import get_system_prompt
from src.utils import memory
from src.database import engine
from sqlalchemy import text
from better_profanity import profanity
import json
import re

# Initialize Mistral Client
client = MistralClient(api_key=settings.MISTRAL_API_KEY)

# Initialize Profanity Filter
profanity.load_censor_words()

def execute_sql_query(query: str):
    """Executes a read-only SQL query and returns the results."""
    # Basic safety check (redundant with prompt instructions but good for defense in depth)
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT", "REVOKE"]
    if any(keyword in query.upper() for keyword in forbidden_keywords):
        return "Error: Unsafe query detected. Only SELECT is allowed."

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            # Convert result to list of dicts
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            return json.dumps(rows, default=str)
    except Exception as e:
        return f"Database Error: {str(e)}"

def process_chat(session_id: str, user_message: str):
    # 1. Profanity Check
    if profanity.contains_profanity(user_message):
        return {
            "response_text": "I cannot respond to that language. Please be polite.",
            "tables_available": [],
            "menu_suggestions": [],
            "navigation_suggestion": None,
            "error": True
        }

    # 2. Retrieve History
    history_data = memory.get_session(session_id)
    
    # Convert history to Mistral ChatMessage objects
    messages = [ChatMessage(role="system", content=get_system_prompt())]
    for msg in history_data:
        messages.append(ChatMessage(role=msg["role"], content=msg["content"]))
    
    # Add current user message
    messages.append(ChatMessage(role="user", content=user_message))

    try:
        # 3. Call Mistral API (First Pass)
        chat_response = client.chat(
            model="mistral-small-latest",
            messages=messages,
        )

        bot_raw_content = chat_response.choices[0].message.content
        
        # 4. Check for Tool Use
        tool_use_match = re.search(r'\{.*"tool_use":\s*"execute_sql".*\}', bot_raw_content, re.DOTALL)
        
        if tool_use_match:
            try:
                tool_data = json.loads(tool_use_match.group(0))
                sql_query = tool_data.get("query")
                
                # Execute SQL
                print(f"Executing SQL: {sql_query}")
                query_result = execute_sql_query(sql_query)
                
                # Add result to messages and call Mistral again
                messages.append(ChatMessage(role="assistant", content=bot_raw_content))
                messages.append(ChatMessage(role="user", content=f"Tool Result: {query_result}"))
                
                # Second Pass
                chat_response = client.chat(
                    model="mistral-small-latest",
                    messages=messages,
                )
                bot_raw_content = chat_response.choices[0].message.content
                
            except json.JSONDecodeError:
                print("Failed to parse tool use JSON")

        # 5. Parse Final JSON Response
        try:
            # Attempt to find JSON block if wrapped in markdown
            json_match = re.search(r"\{.*\}", bot_raw_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed_response = json.loads(json_str)
            else:
                # Try parsing the whole string
                parsed_response = json.loads(bot_raw_content)
                
            # Ensure all fields exist
            response_data = {
                "response_text": parsed_response.get("response_text", "I'm sorry, I couldn't process that."),
                "tables_available": parsed_response.get("tables_available", []),
                "menu_suggestions": parsed_response.get("menu_suggestions", []),
                "navigation_suggestion": parsed_response.get("navigation_suggestion", None),
                "usage": chat_response.usage
            }
            
        except json.JSONDecodeError:
            # Fallback if model didn't return valid JSON
            print(f"JSON Parse Error. Raw content: {bot_raw_content}")
            response_data = {
                "response_text": bot_raw_content, # Fallback to raw text
                "tables_available": [],
                "menu_suggestions": [],
                "navigation_suggestion": None,
                "usage": chat_response.usage
            }

        # 6. Update History
        # We only store the text response in history to keep context clean
        memory.add_message_to_session(session_id, "user", user_message)
        memory.add_message_to_session(session_id, "assistant", response_data["response_text"])
        
        return response_data

    except Exception as e:
        print(f"Error in chat service: {e}")
        return {
            "response_text": "I encountered an error processing your request.",
            "tables_available": [],
            "menu_suggestions": [],
            "navigation_suggestion": None,
            "error": True
        }

        # 5. Return Result
        return {
            "reply": bot_reply,
            "usage": chat_response.usage
        }

    except Exception as e:
        print(f"Mistral API Error: {e}")
        raise Exception("Failed to communicate with AI service.")
