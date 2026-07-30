from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.repositories.meeting_audio_file import create_meeting_audio_file_repo
from app.db.models.meeting_audio import MeetingAudioFile
from app.schema.meeting_audio_file import MeetingAudioFileCreate
from app.core.logger import logger
from app.exceptions.audio_upload import InvalidFileError
from app.services.upload_audio.upload_audio_to_s3 import upload_audio_to_s3

def create_meeting_audio_file_service(user_id: int, meeting_id: int, file: UploadFile, db: Session) -> MeetingAudioFile:
    file_name = file.filename
    if not file_name:
        raise InvalidFileError()
    audio_url = upload_audio_to_s3(file, user_id, meeting_id)
    meeting_audio_file = MeetingAudioFileCreate(
        user_id=user_id,
        meeting_id=meeting_id,
        url=audio_url,
        original_filename=file_name.lower()
    )
    meeting_audio_file_data = create_meeting_audio_file_repo(meeting_audio_file=meeting_audio_file, db=db)
    logger.info("meeting audio file inserted.")
    return meeting_audio_file_data