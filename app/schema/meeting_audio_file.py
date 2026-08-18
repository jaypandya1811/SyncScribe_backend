from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.db.models.meeting_audio import MeetingAudioFileStatus

class MeetingAudioFileBase(BaseModel):
    original_filename: str | None = None

class MeetingAudioFileCreate(MeetingAudioFileBase):
    meeting_id: int
    user_id: int
    url: str

class MeetingSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str

class MeetingAudioFileResponse(MeetingAudioFileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    user_id: int
    url: str
    status: str
    summary: Optional[str] = None
    transcription: Optional[str] = None
    action_items: Optional[List[str]] = None
    meeting: MeetingSummary
    created_at: datetime
    updated_at: datetime

class MeetingAudioFileUpdate(MeetingAudioFileBase):
    id: int
    status: MeetingAudioFileStatus
    transcription: Optional[str] = None
    summary: Optional[str] = None
    action_items: Optional[List[str]] = None
    retry_count: Optional[int] = None