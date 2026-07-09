"""Interaction model — represents meetings/interactions with HCPs."""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    Text,
    JSON,
    Date,
    Time,
)
from sqlalchemy.orm import relationship

from app.database.session import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False, index=True)

    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    visit_type = Column(String(100), nullable=False)  # In-person, Virtual, Phone

    products_discussed = Column(JSON, default=list)
    samples_given = Column(JSON, default=list)

    feedback = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    source = Column(String(50), default="form")  # form, ai
    ai_summary = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="interactions")
    hcp = relationship("HCP", back_populates="interactions")
    history = relationship(
        "InteractionHistory", back_populates="interaction", cascade="all, delete-orphan"
    )
    followup = relationship(
        "Followup",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Interaction id={self.id} user_id={self.user_id} hcp_id={self.hcp_id} date={self.date}>"
