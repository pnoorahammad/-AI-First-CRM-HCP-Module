"""Followup model — represents recommended followups from interactions."""

from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, JSON, Date
from sqlalchemy.orm import relationship

from app.database.session import Base


class Followup(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(
        Integer, ForeignKey("interactions.id"), nullable=False, index=True
    )
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    date = Column(Date, nullable=True, index=True)
    status = Column(String(50), default="pending")  # pending, completed, cancelled
    priority = Column(String(50), default="medium")  # high, medium, low

    notes = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)

    suggested_products = Column(JSON, default=list)
    suggested_questions = Column(JSON, default=list)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    interaction = relationship("Interaction", back_populates="followup")
    hcp = relationship("HCP", back_populates="followups")
    user = relationship("User", back_populates="followups")

    def __repr__(self) -> str:
        return f"<Followup id={self.id} interaction_id={self.interaction_id} date={self.date} status={self.status}>"
