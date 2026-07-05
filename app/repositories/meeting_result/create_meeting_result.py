from sqlalchemy.orm import Session
from app.db.models.meeting_result import MeetingResult
from sqlalchemy.exc import SQLAlchemyError
from app.schema.meeting_results import MeetingResultCreate

def create_meeting_result_repo(meeting_result: MeetingResultCreate, db: Session) -> MeetingResult:
    try:
        meeting_result_data = MeetingResult(**meeting_result.model_dump())
        db.add(meeting_result_data)
        db.commit()
        db.refresh(meeting_result_data)
        return meeting_result_data
    except SQLAlchemyError:
        db.rollback()
        raise