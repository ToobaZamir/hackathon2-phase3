from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database.connection import get_session
from src.models.user import UserRegisterRequest, UserLoginRequest, UserPublic, Token
from src.services.user_service import UserService
from src.core.auth import authenticate_user, create_access_token
from src.core.config import settings
from src.schemas.task import APIResponse, APIErrorResponse
from datetime import timedelta

router = APIRouter()  # Prefix will be added in main.py



@router.post("/sign-up/email", response_model=APIResponse)
def sign_up(user_register: UserRegisterRequest, session: Session = Depends(get_session)):
    # Existing register logic
    existing_user = UserService.get_user_by_username(session, user_register.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    existing_email = UserService.get_user_by_email(session, user_register.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = UserService.create_user(session, user_register)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.username, "user_id": db_user.id},
        expires_delta=access_token_expires
    )
    user_public = UserPublic(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )
    token_response = Token(access_token=access_token, token_type="bearer")
    return APIResponse(
        success=True,
        data={
            "user": user_public.dict(),
            "token": token_response.dict()
        },
        message="User registered successfully"
    )

    


@router.post("/sign-in/email", response_model=APIResponse)
def sign_in(user_login: UserLoginRequest, session: Session = Depends(get_session)):
    # Existing login logic
    user = authenticate_user(session, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )

    user_public = UserPublic(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    token_response = Token(access_token=access_token, token_type="bearer")

    return APIResponse(
        success=True,
        data={
            "user": user_public.dict(),
            "token": token_response.dict()
        },
        message="Login successful"
    )

    


@router.post("/logout", response_model=APIResponse)
def logout():
    """
    Logout user (client-side token disposal)
    """
    return APIResponse(
        success=True,
        message="Logout successful"
    )

from fastapi import Header
from jose import jwt

@router.get("/get-session", response_model=APIResponse)
def get_session_route(authorization: str = Header(None)):
    """
    Get current user session from JWT token
    """
    if not authorization:
        return APIResponse(success=False, message="No session token")
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_info = {
            "username": payload.get("sub"),
            "user_id": payload.get("user_id")
        }
        return APIResponse(success=True, data=user_info, message="Session info")
    except Exception:
        return APIResponse(success=False, message="Invalid session token")
