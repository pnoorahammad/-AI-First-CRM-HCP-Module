"""Interaction CRUD endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.interaction import (
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse,
    InteractionHistoryResponse,
)
from app.services import interaction_service
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])


@router.get("/", response_model=List[InteractionResponse])
def read_interactions(
    hcp_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve interactions for the current user."""
    interactions = interaction_service.get_interactions(
        db, user_id=current_user.id, hcp_id=hcp_id, skip=skip, limit=limit
    )
    return interactions


@router.get("/{interaction_id}", response_model=InteractionResponse)
def read_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a specific interaction."""
    interaction = interaction_service.get_interaction(
        db, interaction_id, current_user.id
    )
    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.post(
    "/", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED
)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Log a new interaction (Structured Form)."""
    return interaction_service.create_interaction(db, interaction, current_user.id)


@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(
    interaction_id: int,
    interaction: InteractionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing interaction."""
    db_interaction = interaction_service.update_interaction(
        db, interaction_id, interaction, current_user.id
    )
    if db_interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return db_interaction


@router.get(
    "/{interaction_id}/history", response_model=List[InteractionHistoryResponse]
)
def read_interaction_history(
    interaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the audit history for a specific interaction."""
    history = interaction_service.get_interaction_history(
        db, interaction_id, current_user.id
    )
    if not history:
        # Check if the interaction exists to return 404 or just empty list
        interaction = interaction_service.get_interaction(
            db, interaction_id, current_user.id
        )
        if not interaction:
            raise HTTPException(status_code=404, detail="Interaction not found")
    return history
