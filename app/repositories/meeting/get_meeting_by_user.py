from sqlalchemy.orm import Session
from app.db.models.meeting import Meeting
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting import MeetingNotFound

def get_meeting_by_user_repo(user_id: int, db: Session) -> list[Meeting]:
    try:
        meeting = db.query(Meeting).filter(Meeting.user_id == user_id).order_by(Meeting.created_at.desc()).all()

        if meeting:
            return meeting
        else:
            raise MeetingNotFound()
    except SQLAlchemyError:
        db.rollback()
        raise