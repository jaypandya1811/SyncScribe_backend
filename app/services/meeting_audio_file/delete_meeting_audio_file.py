from sqlalchemy.orm import Session
from app.repositories.meeting_audio_file import delete_meeting_audio_file_repo
from app.db.models.meeting_audio import MeetingAudioFile
from app.core.logger import logger

def delete_meeting_audio_file_service(audio_file_id: int, db: Session) -> MeetingAudioFile:
    audio_file_data = delete_meeting_audio_file_repo(audio_file_id=audio_file_id, db=db)
    logger.info(f"meeting audio file deleted with id:{audio_file_data}")
    return audio_file_data