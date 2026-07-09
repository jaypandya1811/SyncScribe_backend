from sqlalchemy.orm import Session
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_audio_file import MeetingAudioFileNotFoundError

def get_meeting_audio_file_repo(audio_file_id: int, db: Session) -> MeetingAudioFile:
    try:
        meeting_audio_file = db.get(MeetingAudioFile, audio_file_id)

        if meeting_audio_file:
            return meeting_audio_file
        else:
            raise MeetingAudioFileNotFoundError()
    except SQLAlchemyError:
        db.rollback()
        raise