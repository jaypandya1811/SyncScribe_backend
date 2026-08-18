from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CombinedActionItem(BaseModel):
    task: str
    audio_file_id: int

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
    name: str | None
    summary: str | None
    action_items: list[str] | None
    transcription: str | None
    url: str | None
    status: str
    created_at: datetime
    updated_at: datetime

class MeetingOverviewResponse(BaseModel):
    meeting_id: int
    meeting_name: str
    meeting_type: str | None
    meeting_status: str
    speakers: int | None = None
    description: str | None = None
    audio_files: list[AudioFileSummaryBlock]
    action_items: list[CombinedActionItem]
    action_items_count: int
    audio_file_count: int
    pending_count: int
    created_at: datetime