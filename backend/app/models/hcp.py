"""HCP (Healthcare Professional) model."""

from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship

from app.database.session import Base


class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    hospital = Column(String(255), nullable=True, index=True)
    speciality = Column(String(255), nullable=True, index=True)
    location = Column(String(255), nullable=True, index=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    created_by_user = relationship("User", back_populates="hcps")
    interactions = relationship(
        "Interaction", back_populates="hcp", cascade="all, delete-orphan"
    )
    followups = relationship(
        "Followup", back_populates="hcp", cascade="all, delete-orphan"
    )

    # Composite index for search
    __table_args__ = (Index("ix_hcp_name_hospital", "name", "hospital"),)

    def __repr__(self) -> str:
        return f"<HCP id={self.id} name={self.name} hospital={self.hospital}>"
