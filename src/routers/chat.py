from fastapi import APIRouter, HTTPException
from src.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from src.services import chat_service
from src.utils import memory

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chat_service.process_chat(request.sessionId, request.message)
        if response.get("error"):
            return ChatResponse(
                response_text=response["response_text"], 
                error=True
            )
        
        return ChatResponse(
            response_text=response["response_text"],
            tables_available=response.get("tables_available", []),
            menu_suggestions=response.get("menu_suggestions", []),
            navigation_suggestion=response.get("navigation_suggestion"),
            usage=response.get("usage")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/history/{session_id}")
async def clear_history(session_id: str):
    memory.clear_session(session_id)
    return {"message": f"History cleared for session {session_id}"}
