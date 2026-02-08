"""Service for managing conversations and messages."""
from sqlmodel import Session, select
from typing import List, Dict, Optional
from datetime import datetime

from src.models.conversation import Conversation, ConversationCreate
from src.models.message import Message, MessageCreate, SenderEnum


class ConversationService:
    """Service for conversation and message CRUD operations."""

    def __init__(self, session: Session):
        """Initialize conversation service with database session."""
        self.session = session

    def create_conversation(self, user_id: int) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: ID of the user creating the conversation

        Returns:
            Created conversation object
        """
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(
        self,
        conversation_id: int,
        user_id: int
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID with user authorization check.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user (for authorization)

        Returns:
            Conversation object if found and owned by user, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return self.session.exec(statement).first()

    def get_conversation_history(
        self,
        conversation_id: int,
        limit: Optional[int] = 100
    ) -> List[Dict[str, str]]:
        """
        Fetch all messages for a conversation in chronological order.

        Returns list formatted for Cohere API:
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries with role and content
        """
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        messages = self.session.exec(statement).all()

        return [
            {
                "role": message.sender,
                "content": message.content
            }
            for message in messages
        ]

    def add_message(
        self,
        conversation_id: int,
        sender: str,
        content: str,
    ) -> Message:
        """
        Add a new message to a conversation.

        Args:
            conversation_id: ID of the parent conversation
            sender: Who sent the message ("user" or "ai")
            content: Message content

        Returns:
            Created message object
        """
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            content=content,
        )
        self.session.add(message)

        # Update conversation's updated_at timestamp
        conversation = self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()

        self.session.commit()
        self.session.refresh(message)
        return message

    def get_user_conversations(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            user_id: ID of the user
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip

        Returns:
            List of conversations ordered by most recent first
        """
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.exec(statement).all())
