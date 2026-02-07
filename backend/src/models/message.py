"""Message model for storing chat messages."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, DateTime, JSON, String, func
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class Message(SQLModel, table=True):
    """Message model - represents a single chat message in a conversation."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True, description="Parent conversation")
    role: str = Field(sa_column=Column(String(20), nullable=False), description="Message role (user/assistant/system/tool)")
    content: str = Field(max_length=10000, description="Message content")

    # Optional: Store tool calls for debugging and audit
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON), description="Tool calls metadata")

    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        description="When message was created"
    )

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    """Schema for creating a new message."""
    conversation_id: int
    role: MessageRole
    content: str
    tool_calls: Optional[Dict[str, Any]] = None


class MessagePublic(SQLModel):
    """Public schema for returning message data."""
    id: int
    conversation_id: int
    role: str
    content: str
    tool_calls: Optional[Dict[str, Any]]
    timestamp: datetime

    class Config:
        from_attributes = True
