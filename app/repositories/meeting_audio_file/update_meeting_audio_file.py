from sqlalchemy.orm import Session
from app.db.models.meeting_audio import MeetingAudioFile
from app.schema.meeting_audio_file import MeetingAudioFileUpdate
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_audio_file import MeetingAudioFileUpdateError
from app.repositories.meeting_audio_file.get_meeting_audio_file_by_id import get_meeting_audio_file_repo

def update_meeting_audio_file_repo(audio_file_id: int, meeting_audio_file_update: MeetingAudioFileUpdate, db: Session) -> MeetingAudioFile:
    meeting_audio_file_data = get_meeting_audio_file_repo(audio_file_id=audio_file_id, db=db)
    try:
        update_data = meeting_audio_file_update.model_dump(exclude_unset=True, exclude={"id"})
        for field, value in update_data.items():
            if value is not None:
                setattr(meeting_audio_file_data, field, value)
        db.commit()
        db.refresh(meeting_audio_file_data)
        return meeting_audio_file_data
    except SQLAlchemyError:
        db.rollback()
        raise MeetingAudioFileUpdateError()