"""Authentication dependencies for FastAPI endpoints."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.schemas.user import TokenData
from app.services import user_service

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Dependency to get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("email")
    if email is None:
        raise credentials_exception

    token_data = TokenData(email=email)

    user_dict = user_service.get_user_by_email(email=token_data.email)
    if user_dict is None:
        raise credentials_exception

    if not user_dict.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")

    return User(**user_dict)
