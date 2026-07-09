from sqlalchemy.orm import Session
from app.repositories.meeting_audio_file.get_meeting_audio_file_by_id import get_meeting_audio_file_repo
from app.db.models.meeting_audio import MeetingAudioFile
from app.core.logger import logger

def get_meeting_audio_file_service(audio_file_id: int, db: Session) -> MeetingAudioFile:
    meeting_audio_file_data = get_meeting_audio_file_repo(audio_file_id=audio_file_id, db=db)
    logger.info(f"meeting audio file by id:{meeting_audio_file_data}")
    return meeting_audio_file_data