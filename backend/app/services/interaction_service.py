"""Business logic for Interaction operations."""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.models.interaction import Interaction
from app.models.interaction_history import InteractionHistory
from app.models.followup import Followup
from app.schemas.interaction import InteractionCreate, InteractionUpdate


def get_interactions(
    db: Session,
    user_id: int,
    hcp_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Interaction]:
    """Get interactions for a user, optionally filtered by HCP."""
    query = db.query(Interaction).filter(Interaction.user_id == user_id)

    if hcp_id:
        query = query.filter(Interaction.hcp_id == hcp_id)

    return (
        query.order_by(desc(Interaction.date), desc(Interaction.time))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_interaction(
    db: Session, interaction_id: int, user_id: int
) -> Optional[Interaction]:
    """Get a specific interaction."""
    return (
        db.query(Interaction)
        .filter(Interaction.id == interaction_id, Interaction.user_id == user_id)
        .first()
    )


def create_interaction(
    db: Session, interaction: InteractionCreate, user_id: int
) -> Interaction:
    """Create a new interaction and potential follow-up."""
    # Extract follow_up_date as it goes to a different table conceptually,
    # but we store it for tracking.
    follow_up_date = interaction.follow_up_date

    interaction_data = interaction.model_dump(exclude={"follow_up_date"})

    db_interaction = Interaction(**interaction_data, user_id=user_id)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)

    # Log history
    log_history(db, db_interaction.id, user_id, "create", None, db_interaction)

    # Create follow-up if date provided
    if follow_up_date:
        db_followup = Followup(
            interaction_id=db_interaction.id,
            hcp_id=db_interaction.hcp_id,
            user_id=user_id,
            date=follow_up_date,
            status="pending",
            notes=f"Follow up from interaction on {db_interaction.date}",
        )
        db.add(db_followup)
        db.commit()

    return db_interaction


def update_interaction(
    db: Session,
    interaction_id: int,
    interaction_update: InteractionUpdate,
    user_id: int,
) -> Optional[Interaction]:
    """Update an existing interaction and log history."""
    db_interaction = get_interaction(db, interaction_id, user_id)
    if not db_interaction:
        return None

    # Store old state for history
    old_data = {
        "visit_type": db_interaction.visit_type,
        "products_discussed": db_interaction.products_discussed,
        "samples_given": db_interaction.samples_given,
        "feedback": db_interaction.feedback,
        "notes": db_interaction.notes,
    }

    update_data = interaction_update.model_dump(
        exclude_unset=True, exclude={"follow_up_date"}
    )
    for key, value in update_data.items():
        setattr(db_interaction, key, value)

    db.commit()
    db.refresh(db_interaction)

    # Log history
    log_history(db, db_interaction.id, user_id, "update", old_data, db_interaction)

    # Handle follow-up update if provided
    if interaction_update.follow_up_date:
        followup = (
            db.query(Followup)
            .filter(Followup.interaction_id == db_interaction.id)
            .first()
        )
        if followup:
            followup.date = interaction_update.follow_up_date
        else:
            db_followup = Followup(
                interaction_id=db_interaction.id,
                hcp_id=db_interaction.hcp_id,
                user_id=user_id,
                date=interaction_update.follow_up_date,
                status="pending",
            )
            db.add(db_followup)
        db.commit()

    return db_interaction


def log_history(
    db: Session,
    interaction_id: int,
    user_id: int,
    change_type: str,
    old_data: Optional[dict],
    new_interaction: Interaction,
):
    """Log changes to the interaction_history table."""
    new_data = {
        "visit_type": new_interaction.visit_type,
        "products_discussed": new_interaction.products_discussed,
        "samples_given": new_interaction.samples_given,
        "feedback": new_interaction.feedback,
        "notes": new_interaction.notes,
    }

    history = InteractionHistory(
        interaction_id=interaction_id,
        changed_by=user_id,
        change_type=change_type,
        old_data=old_data,
        new_data=new_data,
    )
    db.add(history)
    db.commit()


def get_interaction_history(
    db: Session, interaction_id: int, user_id: int
) -> List[InteractionHistory]:
    """Get the history log for a specific interaction."""
    # First verify the user owns the interaction
    interaction = get_interaction(db, interaction_id, user_id)
    if not interaction:
        return []

    return (
        db.query(InteractionHistory)
        .filter(InteractionHistory.interaction_id == interaction_id)
        .order_by(desc(InteractionHistory.created_at))
        .all()
    )
