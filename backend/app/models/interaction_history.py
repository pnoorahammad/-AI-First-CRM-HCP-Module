"""Interaction history model — for auditing changes to interactions."""

from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.database.session import Base


class InteractionHistory(Base):
    __tablename__ = "interaction_history"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(
        Integer, ForeignKey("interactions.id"), nullable=False, index=True
    )
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    change_type = Column(String(50), nullable=False)  # create, update

    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    interaction = relationship("Interaction", back_populates="history")
    user = relationship("User")

    def __repr__(self) -> str:
        return f"<InteractionHistory id={self.id} interaction_id={self.interaction_id} change_type={self.change_type}>"
