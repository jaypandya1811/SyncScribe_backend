from sqlalchemy.orm import Session
from app.db.models.meeting import Meeting
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting import MeetingNotFound

def get_meeting_repo(meeting_id: int, db: Session) -> Meeting:
    try:
        meeting = db.get(Meeting, meeting_id)

        if meeting:
            return meeting
        else:
            raise MeetingNotFound()
    except SQLAlchemyError:
        db.rollback()
        raise