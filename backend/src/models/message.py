"""Message model for storing chat messages."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import Column, DateTime, String, func

if TYPE_CHECKING:
    from .conversation import Conversation


class SenderEnum(str, Enum):
    """Who sent the message."""
    USER = "user"
    AI = "ai"


class Message(SQLModel, table=True):
    """A single chat message inside a conversation."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    sender: str = Field(sa_column=Column(String(10), nullable=False))
    content: str = Field(max_length=10000)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    """Schema for creating a new message."""
    conversation_id: int
    sender: SenderEnum
    content: str


class MessagePublic(SQLModel):
    """Public schema for returning message data."""
    id: int
    conversation_id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
