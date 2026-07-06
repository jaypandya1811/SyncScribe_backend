from sqlalchemy.orm import Session
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_audio_file import MeetingAudioFileNotFoundError

def get_meeting_audio_by_user_repo(user_id: int, db: Session) -> list[MeetingAudioFile]:
    try:
        meeting_audio_file_data = db.query(MeetingAudioFile).filter(MeetingAudioFile.user_id == user_id).all()
        if meeting_audio_file_data:
            return meeting_audio_file_data
        else:
            raise MeetingAudioFileNotFoundError()
    except SQLAlchemyError:
        raise