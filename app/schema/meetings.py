from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MeetingCreate(BaseModel):
    name: str
    user_id: int
    type: str
    description: str | None = None

class MeetingUpdate(BaseModel):
    status: str | None = None

class MeetingResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    description: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)