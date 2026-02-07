"""Chat endpoint for conversational task management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any

from backend.src.schemas.chat import ChatRequest, ChatResponse
from backend.src.core.auth import get_current_user
from backend.src.database.connection import get_session
from backend.src.services.conversation_service import ConversationService
from backend.src.models.user import User

router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    user_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Stateless chat endpoint for conversational task management.

    Flow:
    1. Validate JWT and user_id match
    2. Get/create conversation from DB
    3. Fetch full conversation history from DB
    4. Instantiate fresh Cohere agent with MCP tools
    5. Execute agent with history + new message
    6. Save user message and agent response to DB
    7. Return response with conversation_id

    Args:
        user_id: User ID from URL path
        request: Chat request with message and optional conversation_id
        current_user: Authenticated user (from JWT)
        session: Database session

    Returns:
        ChatResponse with agent's message and conversation_id

    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If conversation_id not found
        HTTPException 500: If agent execution fails
    """
    # 1. Validate authorization
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own conversations"
        )

    # 2. Get or create conversation
    conversation_service = ConversationService(session)

    if request.conversation_id:
        conversation = conversation_service.get_conversation(
            conversation_id=request.conversation_id,
            user_id=user_id
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {request.conversation_id} not found"
            )
    else:
        conversation = conversation_service.create_conversation(user_id=user_id)

    # 3. Fetch conversation history from DB
    history = conversation_service.get_conversation_history(conversation.id)

    # 4. Save user message to DB
    user_message = conversation_service.add_message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )

    # 5. Execute agent (placeholder for now - will be replaced in Phase 5)
    # TODO: Replace with actual Cohere agent execution
    agent_response_text = f"[Placeholder] Received your message: '{request.message}'. Agent integration pending."
    tool_calls_log = None

    # Temporary: Echo message until agent is integrated
    if "add" in request.message.lower() or "create" in request.message.lower():
        agent_response_text = "✓ Task creation will be available once the Cohere agent is integrated (Phase 5)."
    elif "list" in request.message.lower() or "show" in request.message.lower():
        agent_response_text = "✓ Task listing will be available once the Cohere agent is integrated (Phase 5)."

    # 6. Save agent response to DB
    assistant_message = conversation_service.add_message(
        conversation_id=conversation.id,
        role="assistant",
        content=agent_response_text,
        tool_calls=tool_calls_log
    )

    # 7. Return response
    return ChatResponse(
        message=agent_response_text,
        conversation_id=conversation.id,
        tool_calls=tool_calls_log
    )
