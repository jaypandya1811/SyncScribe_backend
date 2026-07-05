from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MeetingCreate(BaseModel):
    name: str
    audio_url: str | None = None
    user_id: int

class MeetingUpdate(BaseModel):
    meeting_url: str | None = None
    status: str | None = None

class MeetingResponse(BaseModel):
    id: int
    user_id: int
    name: str
    audio_url: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)