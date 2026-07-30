from app.db.database import Base
from sqlalchemy import String, Text, ForeignKey, DateTime
from enum import Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .meeting import Meeting
    from .user import User

class MeetingAudioFileStatus(str, Enum):
    UPLOADED = "uploaded"
    TRANSCRIPT_FAILED = "transcript_failed"
    TRANSCRIBED = "transcribed"
    SUMMARIZATION_FAILED = "summarization_failed"
    SUMMARIZED = "summarized"

class MeetingAudioFile(Base):
    __tablename__ = "meeting_audio_files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    original_filename: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    transcription: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_items: Mapped[list[dict[str, Any]] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default=MeetingAudioFileStatus.UPLOADED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    meeting: Mapped["Meeting"] = relationship(back_populates="audio_files")
    user: Mapped["User"] = relationship()