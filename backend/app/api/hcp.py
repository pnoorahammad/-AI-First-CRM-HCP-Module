"""HCP CRUD endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPResponse
from app.services import hcp_service
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/hcp", tags=["HCPs"])


@router.get("/", response_model=List[HCPResponse])
def read_hcps(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all HCPs with optional search."""
    hcps = hcp_service.get_hcps(db, skip=skip, limit=limit, search=search)
    return hcps


@router.get("/{hcp_id}", response_model=HCPResponse)
def read_hcp(
    hcp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a specific HCP by ID."""
    db_hcp = hcp_service.get_hcp(db, hcp_id)
    if db_hcp is None:
        raise HTTPException(status_code=404, detail="HCP not found")
    return db_hcp


@router.post("/", response_model=HCPResponse, status_code=status.HTTP_201_CREATED)
def create_hcp(
    hcp: HCPCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new HCP."""
    return hcp_service.create_hcp(db, hcp, user_id=current_user.id)


@router.put("/{hcp_id}", response_model=HCPResponse)
def update_hcp(
    hcp_id: int,
    hcp: HCPUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an HCP."""
    db_hcp = hcp_service.update_hcp(db, hcp_id, hcp)
    if db_hcp is None:
        raise HTTPException(status_code=404, detail="HCP not found")
    return db_hcp


@router.delete("/{hcp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hcp(
    hcp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an HCP."""
    success = hcp_service.delete_hcp(db, hcp_id)
    if not success:
        raise HTTPException(status_code=404, detail="HCP not found")
    return None
