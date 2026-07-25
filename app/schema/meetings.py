from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MeetingCreate(BaseModel):
    name: str
    user_id: int
    type: str
    speakers: int | None = None
    description: str | None = None

class MeetingUpdate(BaseModel):
    status: str | None = None

class MeetingResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    speakers: int | None = None
    description: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AudioFileSummaryBlock(BaseModel):
    audio_file_id: int
    name: str
    summary: str | None
    status: str

class MeetingOverviewResponse(BaseModel):
    meeting_id: int
    meeting_name: str
    meeting_type: str
    meeting_status: str
    speakers: int | None = None
    summaries: list[AudioFileSummaryBlock]
    action_items: list[dict]
    action_items_count: int
    audio_file_count: int
    pending_count: int
    created_at: str