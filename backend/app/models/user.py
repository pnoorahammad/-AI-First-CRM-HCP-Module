"""User model — represents CRM field representatives."""

from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship

from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="rep", nullable=False)  # rep, manager, admin
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    hcps = relationship(
        "HCP", back_populates="created_by_user", cascade="all, delete-orphan"
    )
    interactions = relationship(
        "Interaction", back_populates="user", cascade="all, delete-orphan"
    )
    followups = relationship(
        "Followup", back_populates="user", cascade="all, delete-orphan"
    )
    ai_logs = relationship("AILog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
