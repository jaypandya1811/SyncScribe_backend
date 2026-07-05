from sqlalchemy.orm import Session
from app.db.models.meeting import Meeting
from app.schema.meetings import MeetingUpdate
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting import MeetingUpdateError, MeetingNotFound
from app.repositories.meeting.get_meeting_by_id import get_meeting_repo

def update_meeting_repo(meeting_id: int, meeting: MeetingUpdate, db: Session) -> Meeting:
    meeting_data = get_meeting_repo(meeting_id=meeting_id, db=db)
    if not meeting_data:
        raise MeetingNotFound()
    
    try:
        for key, value in meeting.model_dump(exclude_unset=True).items():
            setattr(meeting_data, key, value)
        db.commit()
        db.refresh(meeting_data)
        return meeting_data
    except SQLAlchemyError:
        db.rollback()
        raise MeetingUpdateError()