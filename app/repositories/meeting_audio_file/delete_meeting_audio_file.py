from sqlalchemy.orm import Session
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_audio_file import MeetingAudioFileNotFoundError

def delete_meeting_audio_file_repo(audio_file_id: int, db: Session) -> MeetingAudioFile:
    try:
        audio_file = db.get(MeetingAudioFile, audio_file_id)

        if audio_file:
            db.delete(audio_file)
            db.commit()
            return audio_file
        else:
            raise MeetingAudioFileNotFoundError()
    except SQLAlchemyError:
        db.rollback()
        raise