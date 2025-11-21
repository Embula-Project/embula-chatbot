from typing import List, Dict
from sqlalchemy.orm import Session
from src.models.models import ChatHistory
from src.database import SessionLocal, engine, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

MAX_HISTORY_LENGTH = 10

def get_session(session_id: str) -> List[Dict[str, str]]:
    db: Session = SessionLocal()
    try:
        # Fetch last N messages for context
        history = db.query(ChatHistory)\
            .filter(ChatHistory.session_id == session_id)\
            .order_by(ChatHistory.timestamp.asc())\
            .all()
        
        # Convert to format expected by Mistral/Service
        # We might want to limit this if the DB gets huge, but for now we take all 
        # or implement a limit in the query if needed.
        # Taking last MAX_HISTORY_LENGTH messages
        recent_history = history[-MAX_HISTORY_LENGTH:] if len(history) > MAX_HISTORY_LENGTH else history
        
        return [{"role": msg.role, "content": msg.content} for msg in recent_history]
    finally:
        db.close()

def add_message_to_session(session_id: str, role: str, content: str):
    db: Session = SessionLocal()
    try:
        new_message = ChatHistory(session_id=session_id, role=role, content=content)
        db.add(new_message)
        db.commit()
    finally:
        db.close()

def clear_session(session_id: str):
    db: Session = SessionLocal()
    try:
        db.query(ChatHistory).filter(ChatHistory.session_id == session_id).delete()
        db.commit()
    finally:
        db.close()
