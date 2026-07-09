"""Authentication and User registration endpoints."""

from datetime import timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services import user_service
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return user_service.create_user(user_in)


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = user_service.authenticate_user(user_in)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"], "role": user["role"]},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
