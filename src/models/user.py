from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, func
from src.core.security import verify_password as verify_password_func, get_password_hash
import os


class UserBase(SQLModel):
    """Base model for User containing common fields"""
    username: str = Field(unique=True, min_length=3, max_length=50)
    email: str = Field(unique=True, min_length=5, max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)


class User(UserBase, table=True):
    """User model for database table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    ))
    updated_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    ))

    def verify_password(self, plain_password: str) -> bool:
        """Verify a password against the hashed password"""
        return verify_password_func(plain_password, self.hashed_password)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(min_length=6, max_length=128)

    def hash_password(self) -> str:
        """Hash the password before storing"""
        return get_password_hash(self.password)


class UserRegisterRequest(UserCreate):
    """Schema for user registration request"""
    pass


class UserLoginRequest(SQLModel):
    """Schema for user login request"""
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserPublic(UserBase):
    """Public schema for returning user data without sensitive info"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """Schema for updating user information"""
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[str] = Field(default=None, min_length=5, max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)


class Token(SQLModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    """Schema for token data payload"""
    username: Optional[str] = None
    user_id: Optional[int] = None