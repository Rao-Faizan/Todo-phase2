from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import Session
from typing import Annotated
from models.user import User, UserCreate, UserResponse
from services.auth_service import create_user, authenticate_user
from database import get_session
from schemas.auth import LoginRequest, LoginResponse
from datetime import timedelta
from utils.jwt import create_access_token
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create limiter for auth routes
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/signup", response_model=LoginResponse)
@limiter.limit("100/minute")
async def signup(request: Request, user_data: UserCreate, session: Session = Depends(get_session)):
    """Create a new user account and return token"""
    try:
        user = await create_user(user_data, session)

        # Create JWT access token
        access_token_expires = timedelta(minutes=1440)  # 24 hours
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        return LoginResponse(user=UserResponse.from_orm(user), token=access_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin", response_model=LoginResponse)
@limiter.limit("100/minute")
async def signin(request: Request, login_data: LoginRequest, session: Session = Depends(get_session)):
    """Authenticate user and return token"""
    user = await authenticate_user(login_data.email, login_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT access token
    access_token_expires = timedelta(minutes=1440)  # 24 hours
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return LoginResponse(user=UserResponse.from_orm(user), token=access_token)