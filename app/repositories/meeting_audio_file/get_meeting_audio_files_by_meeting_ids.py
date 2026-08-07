from sqlalchemy.orm import Session
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError

def get_meeting_audio_fiels_by_meeting_ids_repo(meeting_ids: list[int], db: Session) -> list[MeetingAudioFile]:
    try:
        meeting_audio_file_data = (
            db.query(MeetingAudioFile)
            .filter(MeetingAudioFile.meeting_id.in_(meeting_ids))
            .order_by(MeetingAudioFile.meeting_id.asc(), MeetingAudioFile.created_at.asc())
            .all()
        )
        if meeting_audio_file_data:
            return meeting_audio_file_data
        else:
            return []
    except SQLAlchemyError:
        raise