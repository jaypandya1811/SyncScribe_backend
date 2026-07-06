from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class MeetingAudioFileStatus(str, Enum):
    UPLOADED = "uploaded"
    TRANSCRIPT_FAILED = "transcript_failed"
    TRANSCRIBED = "transcribed"
    SUMMARIZATION_FAILED = "summarization_failed"
    SUMMARIZED = "summarized"

class MeetingAudioFile(Base):
    __tablename__ = "meeting_audio_files"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)
    original_filename = Column(String, nullable=True)
    transcription = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    action_items = Column(JSONB, nullable=True)
    status = Column(String, nullable=False, default=MeetingAudioFileStatus.UPLOADED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())