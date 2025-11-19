import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Interval, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base

from enum import Enum as PyEnum

class ShiftStatus(PyEnum):
    running = "running"
    paused = "paused"
    stopped = "stopped"

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(ShiftStatus, name="shift_status"), nullable=False, default=ShiftStatus.running)
    duration = Column(Interval, nullable=True)  # computed when stopped
    # relationships
    user = relationship("User", backref="shifts")
