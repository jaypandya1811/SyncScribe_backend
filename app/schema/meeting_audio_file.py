from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MeetingAudioFileBase(BaseModel):
    original_filename: str | None = None

class MeetingAudioFileCreate(MeetingAudioFileBase):
    meeting_id: int
    user_id: int
    url: str

class MeetingAudioFileResponse(MeetingAudioFileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    user_id: int
    url: str
    created_at: datetime
    updated_at: datetime