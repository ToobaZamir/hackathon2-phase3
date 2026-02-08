"""Chat endpoint for conversational task management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.schemas.chat import ChatRequest, ChatResponse
from src.core.auth import get_current_user
from src.database.connection import get_session
from src.services.conversation_service import ConversationService
from src.services.chatbot_service import ChatbotService
from src.models.user import User

router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    user_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ChatResponse:
    """
    Stateless chat endpoint for conversational task management.

    Flow:
    1. Validate JWT and user_id match
    2. Get/create conversation from DB
    3. Delegate to ChatbotService (history → save user msg → AI → save AI msg)
    4. Return response with conversation_id
    """
    # 1. Validate authorization
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own conversations",
        )

    # 2. Get or create conversation
    conversation_service = ConversationService(session)

    if request.conversation_id:
        conversation = conversation_service.get_conversation(
            conversation_id=request.conversation_id,
            user_id=user_id,
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {request.conversation_id} not found",
            )
    else:
        conversation = conversation_service.create_conversation(user_id=user_id)

    # 3. Run the full chat cycle via ChatbotService
    chatbot = ChatbotService(session)

    try:
        result = await chatbot.handle_message(
            conversation_id=conversation.id,
            user_id=user_id,
            user_message=request.message,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

    # 4. Return response
    return ChatResponse(
        message=result["ai_response"],
        conversation_id=result["conversation_id"],
    )
