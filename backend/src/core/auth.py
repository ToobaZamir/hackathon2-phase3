from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from src.models.user import User, TokenData
from src.database.connection import get_session
from src.core.config import settings
from src.core.security import verify_password, get_password_hash
from src.services.user_service import UserService

# Initialize JWT context
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token with the given data and expiration time

    Args:
        data: Dictionary containing the claims to be encoded in the token
        expires_delta: Optional timedelta for token expiration (uses default if not provided)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """
    Verify the JWT token and extract the token data

    Args:
        token: JWT token string to verify
        credentials_exception: HTTPException to raise if token is invalid

    Returns:
        TokenData object with the decoded token information
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            raise credentials_exception

        token_data = TokenData(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user from the token

    Args:
        credentials: HTTP authorization credentials from the request
        session: Database session for querying user

    Returns:
        User object for the authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(credentials.credentials, credentials_exception)

    user = UserService.get_user_by_username(session, token_data.username)

    if user is None:
        raise credentials_exception

    return user


def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by checking username and password

    Args:
        session: Database session for querying user
        username: Username to authenticate
        password: Plain text password to verify

    Returns:
        User object if authentication successful, None otherwise
    """
    user = UserService.get_user_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user