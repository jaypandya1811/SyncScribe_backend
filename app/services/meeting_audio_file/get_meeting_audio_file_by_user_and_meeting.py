from sqlalchemy.orm import Session
from app.repositories.meeting_audio_file import get_meeting_audio_by_meeting_and_user_repo
from app.db.models.meeting_audio import MeetingAudioFile
from app.core.logger import logger

def get_meeting_audio_file_by_meeting_and_user_service(meeting_id: int, user_id: int,db: Session) -> list[MeetingAudioFile]:
    meeting_audio_file_data = get_meeting_audio_by_meeting_and_user_repo(meeting_id=meeting_id, user_id=user_id,db=db)
    logger.info(f"meetings by user id:{meeting_audio_file_data}")
    return meeting_audio_file_data