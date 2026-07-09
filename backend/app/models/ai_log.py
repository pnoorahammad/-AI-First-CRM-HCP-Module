"""AI Log model — tracks AI agent usage, interactions, and metrics."""

from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database.session import Base


class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(100), nullable=False, index=True)

    input_text = Column(Text, nullable=False)
    output_text = Column(Text, nullable=True)

    tool_used = Column(String(100), nullable=True)
    model_used = Column(String(100), nullable=True)

    tokens_used = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user = relationship("User", back_populates="ai_logs")

    def __repr__(self) -> str:
        return (
            f"<AILog id={self.id} user_id={self.user_id} session_id={self.session_id}>"
        )
