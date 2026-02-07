"""Chat request and response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's message to the agent"
    )
    conversation_id: Optional[int] = Field(
        None,
        description="Existing conversation ID (if resuming). If null, creates new conversation."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add buy groceries",
                "conversation_id": 123
            }
        }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    message: str = Field(
        ...,
        description="Agent's response message"
    )
    conversation_id: int = Field(
        ...,
        description="Conversation ID (for subsequent requests)"
    )
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of tools called by the agent (for debugging)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "✓ Added task: Buy groceries",
                "conversation_id": 123,
                "tool_calls": [
                    {
                        "tool": "create_task",
                        "arguments": {"user_id": 1, "title": "Buy groceries"},
                        "result": {"success": True, "task_id": 456}
                    }
                ]
            }
        }
