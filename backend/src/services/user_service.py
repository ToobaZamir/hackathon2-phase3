from sqlmodel import Session, select
from typing import Optional
from src.models.user import User, UserCreate, UserUpdate
from src.core.security import get_password_hash


class UserService:
    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """Get a user by their ID"""
        return session.get(User, user_id)

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[User]:
        """Get a user by their username"""
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get a user by their email"""
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """Create a new user with hashed password"""
        # Hash the password
        hashed_password = user_create.hash_password()

        # Create user object with hashed password
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(session: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        db_user = session.get(User, user_id)
        if not db_user:
            return None

        # Update fields if provided
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.first_name is not None:
            db_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            db_user.last_name = user_update.last_name

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def deactivate_user(session: Session, user_id: int) -> bool:
        """Deactivate a user account"""
        db_user = session.get(User, user_id)
        if not db_user:
            return False

        db_user.is_active = False
        session.add(db_user)
        session.commit()
        return True