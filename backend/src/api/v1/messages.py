"""Message endpoints for conversation message management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from src.database.connection import get_session
from src.core.auth import get_current_user
from src.models.user import User
from src.models.message import Message, MessagePublic, SenderEnum
from src.services.conversation_service import ConversationService
from sqlmodel import SQLModel


class MessageCreateRequest(SQLModel):
    """Request body for creating a message (conversation_id comes from path)."""
    sender: SenderEnum
    content: str


router = APIRouter()


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessagePublic,
    status_code=status.HTTP_201_CREATED,
)
def add_message(
    conversation_id: int,
    body: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Add a message to a conversation.

    The authenticated user must own the conversation.
    Sender must be "user" or "ai".
    """
    conversation_service = ConversationService(session)
    conversation = conversation_service.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )

    message = conversation_service.add_message(
        conversation_id=conversation_id,
        sender=body.sender.value,
        content=body.content,
    )

    return message


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=List[MessagePublic],
)
def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Get all messages in a conversation ordered by creation time.

    The authenticated user must own the conversation.
    """
    conversation_service = ConversationService(session)
    conversation = conversation_service.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )

    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = session.exec(statement).all()

    return messages
