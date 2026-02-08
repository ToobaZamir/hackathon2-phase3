"""Conversation endpoints for managing chat sessions."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func
from typing import List

from src.database.db import get_session
from src.core.auth import get_current_user
from src.models.user import User
from src.models.conversation import Conversation, ConversationPublic
from src.models.message import Message
from src.services.conversation_service import ConversationService

router = APIRouter()


@router.post(
    "/conversations",
    response_model=ConversationPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a new conversation for the authenticated user."""
    conversation_service = ConversationService(session)
    conversation = conversation_service.create_conversation(user_id=current_user.id)

    return ConversationPublic(
        id=conversation.id,
        user_id=conversation.user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=0,
    )


@router.get(
    "/conversations",
    response_model=List[ConversationPublic],
)
def list_conversations(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List all conversations for the authenticated user (most recent first)."""
    conversation_service = ConversationService(session)
    conversations = conversation_service.get_user_conversations(
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )

    results: List[ConversationPublic] = []
    for conv in conversations:
        count = session.exec(
            select(func.count())
            .select_from(Message)
            .where(Message.conversation_id == conv.id)
        ).one()

        results.append(
            ConversationPublic(
                id=conv.id,
                user_id=conv.user_id,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=count,
            )
        )

    return results


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationPublic,
)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a single conversation by ID (must be owned by the authenticated user)."""
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

    count = session.exec(
        select(func.count())
        .select_from(Message)
        .where(Message.conversation_id == conversation.id)
    ).one()

    return ConversationPublic(
        id=conversation.id,
        user_id=conversation.user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=count,
    )
