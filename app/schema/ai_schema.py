from pydantic import BaseModel
from typing import List

class SummaryResult(BaseModel):
    summary: str
    action_items: List[str]

class TranscriptionResult(BaseModel):
    text: str
    segments: list = []