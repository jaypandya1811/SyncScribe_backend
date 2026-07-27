from sqlalchemy.orm import Session
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_audio_file import MeetingAudioFileNotFoundError

def get_meeting_audio_by_meeting_repo(meeting_id: int, db: Session) -> list[MeetingAudioFile]:
    try:
        meeting_audio_file_data = db.query(MeetingAudioFile).filter(MeetingAudioFile.meeting_id == meeting_id).order_by(MeetingAudioFile.created_at.asc()).all()
        if meeting_audio_file_data:
            return meeting_audio_file_data
        else:
            return []
    except SQLAlchemyError:
        raise MeetingAudioFileNotFoundError()