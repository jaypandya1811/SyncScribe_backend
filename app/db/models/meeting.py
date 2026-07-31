from app.db.database import Base
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING, Optional
from datetime import datetime
if TYPE_CHECKING:
    from .user import User
from .meeting_audio import MeetingAudioFile

class MeetingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"

class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    speakers: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default=MeetingStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="meetings")
    audio_files: Mapped[list["MeetingAudioFile"]] = relationship(back_populates="meeting", cascade="all, delete-orphan")