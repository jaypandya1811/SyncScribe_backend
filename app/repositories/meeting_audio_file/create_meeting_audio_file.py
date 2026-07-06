from sqlalchemy.orm import Session
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError
from app.schema.meeting_audio_file import MeetingAudioFileCreate

def create_meeting_audio_file_repo(meeting_audio_file: MeetingAudioFileCreate, db: Session) -> MeetingAudioFile:
    try:
        db_meeting_audio_file = MeetingAudioFile(**meeting_audio_file.model_dump())
        db.add(db_meeting_audio_file)
        db.commit()
        db.refresh(db_meeting_audio_file)
        return db_meeting_audio_file
    except SQLAlchemyError:
        db.rollback()
        raise