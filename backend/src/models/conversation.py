"""Conversation model for storing chat sessions."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, DateTime, func


class Conversation(SQLModel, table=True):
    """Conversation model - represents a chat session between user and AI agent."""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, description="Owner of the conversation")

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        description="When conversation was created"
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
        description="Last activity timestamp"
    )

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ConversationCreate(SQLModel):
    """Schema for creating a new conversation."""
    user_id: int


class ConversationPublic(SQLModel):
    """Public schema for returning conversation data."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    message_count: int = 0  # Computed field

    class Config:
        from_attributes = True
