from sqlalchemy.orm import Session
from app.repositories.meeting_audio_file import update_meeting_audio_file_repo
from app.db.models.meeting_audio import MeetingAudioFile
from app.schema.meeting_audio_file import MeetingAudioFileUpdate
from app.db.models.meeting_audio import MeetingAudioFileStatus
from typing import Optional, List, Dict, Any
from app.core.logger import logger

def update_meeting_audio_file_service(
    id: int,
    status: MeetingAudioFileStatus,
    transcription: Optional[str],
    summary: Optional[str],
    action_items: Optional[List[Dict[str, Any]]],
    db: Session,) -> MeetingAudioFile:

    meeting_audio_file_update = MeetingAudioFileUpdate(
        id=id,
        status=status,
        transcription=transcription,
        summary=summary,
        action_items=action_items,
    )
    meeting_audio_file_data = update_meeting_audio_file_repo(audio_file_id=meeting_audio_file_update.id, meeting_audio_file_update=meeting_audio_file_update, db=db)
    logger.info(f"meeting audio file data updated: {meeting_audio_file_data}")
    return meeting_audio_file_data