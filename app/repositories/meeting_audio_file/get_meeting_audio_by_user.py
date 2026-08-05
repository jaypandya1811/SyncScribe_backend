from sqlalchemy.orm import Session, joinedload
from app.db.models.meeting_audio import MeetingAudioFile
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_audio_file import MeetingAudioFileNotFoundError

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

        print("Repository:", len(result))
        print([r.id for r in result])

        return result

    except SQLAlchemyError:
        raise