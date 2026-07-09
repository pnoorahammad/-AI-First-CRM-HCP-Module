"""Chat and AI endpoints."""

import uuid
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import chat_service
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/chat", tags=["Chat & AI"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str
    session_id: str
    tools_used: List[str] = []


@router.post("/", response_model=ChatResponse)
def process_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Process a message using the LangGraph AI agent."""
    session_id = request.session_id or str(uuid.uuid4())

    # Convert Pydantic models to dicts for the service
    history_dicts = [
        {"role": msg.role, "content": msg.content} for msg in request.history
    ]

    try:
        result = chat_service.process_chat_message(
            db=db,
            user_id=current_user.id,
            session_id=session_id,
            message=request.message,
            history=history_dicts,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
