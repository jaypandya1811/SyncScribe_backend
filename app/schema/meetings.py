from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MeetingCreate(BaseModel):
    name: str
    user_id: int

class MeetingUpdate(BaseModel):
    status: str | None = None

class MeetingResponse(BaseModel):
    id: int
    user_id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)