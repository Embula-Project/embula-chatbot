from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from src.config import settings
from src.utils import memory
from better_profanity import profanity
import datetime

# Initialize Mistral Client
# Note: Using sync client for simplicity, but in high-load production, 
# consider using MistralAsyncClient or running in a threadpool.
client = MistralClient(api_key=settings.MISTRAL_API_KEY)

# Initialize Profanity Filter
profanity.load_censor_words()

SYSTEM_PROMPT = f"""You are the official AI assistant for Embula Restaurant. 
Your goal is to be friendly, helpful, and strictly answer questions related to the restaurant, its menu, hours, and reservations.
Do not hallucinate or make up facts. If you don't know something, say you don't know and suggest contacting the restaurant directly.
Keep responses concise and structured.
Current date: {datetime.date.today()}"""

def process_chat(session_id: str, user_message: str):
    # 1. Profanity Check
    if profanity.contains_profanity(user_message):
        return {
            "reply": "I cannot respond to that language. Please be polite.",
            "error": True
        }

    # 2. Retrieve History
    history_data = memory.get_session(session_id)
    
    # Convert history to Mistral ChatMessage objects
    messages = [ChatMessage(role="system", content=SYSTEM_PROMPT)]
    for msg in history_data:
        messages.append(ChatMessage(role=msg["role"], content=msg["content"]))
    
    # Add current user message
    messages.append(ChatMessage(role="user", content=user_message))

    try:
        # 3. Call Mistral API
        chat_response = client.chat(
            model="mistral-small-latest",
            messages=messages,
        )

        bot_reply = chat_response.choices[0].message.content

        # 4. Update History
        memory.add_message_to_session(session_id, "user", user_message)
        memory.add_message_to_session(session_id, "assistant", bot_reply)

        # 5. Return Result
        return {
            "reply": bot_reply,
            "usage": chat_response.usage
        }

    except Exception as e:
        print(f"Mistral API Error: {e}")
        raise Exception("Failed to communicate with AI service.")
