"""Business logic for HCP operations."""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate


def get_hcps(
    db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None
) -> List[HCP]:
    """Get list of HCPs with optional search."""
    query = db.query(HCP)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                HCP.name.ilike(search_term),
                HCP.hospital.ilike(search_term),
                HCP.speciality.ilike(search_term),
                HCP.location.ilike(search_term),
            )
        )

    return query.offset(skip).limit(limit).all()


def get_hcp(db: Session, hcp_id: int) -> Optional[HCP]:
    """Get a specific HCP by ID."""
    return db.query(HCP).filter(HCP.id == hcp_id).first()


def create_hcp(db: Session, hcp: HCPCreate, user_id: int) -> HCP:
    """Create a new HCP."""
    db_hcp = HCP(**hcp.model_dump(), created_by=user_id)
    db.add(db_hcp)
    db.commit()
    db.refresh(db_hcp)
    return db_hcp


def update_hcp(db: Session, hcp_id: int, hcp_update: HCPUpdate) -> Optional[HCP]:
    """Update an existing HCP."""
    db_hcp = get_hcp(db, hcp_id)
    if not db_hcp:
        return None

    update_data = hcp_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hcp, key, value)

    db.commit()
    db.refresh(db_hcp)
    return db_hcp


def delete_hcp(db: Session, hcp_id: int) -> bool:
    """Delete an HCP."""
    db_hcp = get_hcp(db, hcp_id)
    if not db_hcp:
        return False

    db.delete(db_hcp)
    db.commit()
    return True
