"""Business logic for User operations — backed by Supabase HTTPS API."""

from fastapi import HTTPException, status
from typing import Optional

from app.core.security import hash_password, verify_password
from app.database.session import get_supabase


def get_user_by_email(email: str) -> Optional[dict]:
    """Retrieve a user from Supabase by email."""
    sb = get_supabase()
    result = sb.table("users").select("*").eq("email", email).limit(1).execute()
    return result.data[0] if result.data else None


def get_user_by_id(user_id: int) -> Optional[dict]:
    """Retrieve a user from Supabase by ID."""
    sb = get_supabase()
    result = sb.table("users").select("*").eq("id", user_id).limit(1).execute()
    return result.data[0] if result.data else None


def create_user(user_in) -> dict:
    """Create a new user in Supabase."""
    if get_user_by_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(user_in.password)
    sb = get_supabase()
    result = (
        sb.table("users")
        .insert(
            {
                "email": user_in.email,
                "full_name": user_in.full_name,
                "role": (
                    user_in.role if hasattr(user_in, "role") and user_in.role else "rep"
                ),
                "hashed_password": hashed_password,
                "is_active": True,
            }
        )
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user",
        )
    return result.data[0]


def authenticate_user(user_login) -> dict:
    """Authenticate a user by email and password."""
    user = get_user_by_email(user_login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(user_login.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return user
