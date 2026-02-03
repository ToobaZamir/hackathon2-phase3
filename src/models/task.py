from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, func
from enum import Enum

class TaskBase(SQLModel):
    """Base model for Task containing common fields"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(index=True)

class Task(TaskBase, table=True):
    """Task model for database table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False))

class TaskUpdate(SQLModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)

    class Config:
        from_attributes = True

class TaskCreate(TaskBase):
    """Schema for creating a new task - inherits all fields from TaskBase"""
    pass

class TaskPublic(TaskBase):
    """Public schema for returning task data"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskPatch(SQLModel):
    """Schema for patching task completion status"""
    completed: bool