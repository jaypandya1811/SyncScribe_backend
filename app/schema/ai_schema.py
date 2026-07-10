from pydantic import BaseModel
from typing import Optional, List

class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = None
    due_date: Optional[str] = None

class SummaryResult(BaseModel):
    summary: str
    action_items: List[ActionItem]

class TranscriptionResult(BaseModel):
    text: str
    segments: list = []