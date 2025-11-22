from pydantic import BaseModel
from typing import Optional, Any, List

class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = "default-session"

class ChatResponse(BaseModel):
    response_text: str
    tables_available: Optional[List[Any]] = []
    menu_suggestions: Optional[List[Any]] = []
    navigation_suggestion: Optional[str] = None
    usage: Optional[Any] = None
    error: Optional[bool] = False

class ErrorResponse(BaseModel):
    error: str
