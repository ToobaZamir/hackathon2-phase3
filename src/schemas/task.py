from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Already defined in models/task.py, but we'll create additional response schemas here

class TaskResponse(BaseModel):
    """Response schema for task operations"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

class TaskCreateRequest(BaseModel):
    """Request schema for creating a task"""
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskListResponse(BaseModel):
    """Response schema for listing tasks"""
    tasks: List[TaskResponse]
    total: int

class TaskCompletionRequest(BaseModel):
    """Request schema for updating task completion status"""
    completed: bool

class APIResponse(BaseModel):
    """Generic API response schema"""
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None

class APIErrorResponse(BaseModel):
    """Generic API error response schema"""
    success: bool
    error: dict