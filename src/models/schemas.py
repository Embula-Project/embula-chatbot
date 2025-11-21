from pydantic import BaseModel
from typing import Optional, Any

class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = "default-session"

class ChatResponse(BaseModel):
    reply: str
    usage: Optional[Any] = None
    error: Optional[bool] = False

class ErrorResponse(BaseModel):
    error: str
