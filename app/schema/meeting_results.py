from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

class MeetingResultCreate(BaseModel):
    meeting_id: int
    transcription: str | None = None
    summary: str | None = None
    action_items: list[dict[str, Any]] | None = None

class MeetingResultUpdate(BaseModel):
    transcription: str | None = None
    summary: str | None = None
    action_items: list[dict[str, Any]] | None = None

class MeetingResultResponse(BaseModel):
    id: int
    meeting_id: int
    transcription: str | None
    summary: str | None
    action_items: list[dict[str, Any]] | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)