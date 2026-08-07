from sqlalchemy.orm import Session, joinedload
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError

def get_meeting_audio_by_user_repo(user_id: int, status: str | None,db: Session) -> list[MeetingAudioFile]:
    try:
        query =(
        db.query(MeetingAudioFile)
        .options(joinedload(MeetingAudioFile.meeting))
        .filter(MeetingAudioFile.user_id == user_id)
        ) 

        if status is not None:
            query = query.filter(
                MeetingAudioFile.status == status
            )

        result = query.all()

        return result

    except SQLAlchemyError:
        raise