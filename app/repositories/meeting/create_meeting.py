from sqlalchemy.orm import Session
from app.db.models.meeting import Meeting
from sqlalchemy.exc import SQLAlchemyError
from app.schema.meetings import MeetingCreate

def create_meeting_repo(meeting: MeetingCreate, db: Session) -> Meeting:
    try:
        db_meeting = Meeting(**meeting.model_dump())
        db.add(db_meeting)
        db.commit()
        db.refresh(db_meeting)
        return db_meeting
    except SQLAlchemyError:
        db.rollback()
        raise