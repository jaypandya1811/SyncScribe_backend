from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.repositories.meeting import create_meeting_repo
from app.db.models.meeting import Meeting
from app.schema.meetings import MeetingCreate
from app.exceptions.user import UserNotFoundError
from app.core.logger import logger
from app.services.upload_audio.upload_audio_to_s3 import upload_audio_to_s3

def create_meeting_service(user_id: int, name: str, type: str, description: str | None, speakers: int | None, db: Session) -> Meeting:
    meeting = MeetingCreate(
        user_id=user_id,
        name=name,
        type=type,
        speakers=speakers,
        description=description,
    )
    meeting_data = create_meeting_repo(meeting=meeting, db=db)
    logger.info("meeting created.")
    return meeting_data