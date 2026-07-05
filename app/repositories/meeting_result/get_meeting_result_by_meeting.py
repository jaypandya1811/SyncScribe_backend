from sqlalchemy.orm import Session
from app.db.models.meeting_result import MeetingResult
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_result import MeetingResultNotFound

def get_meeting_result_by_meeting_repo(meeting_id: int, db: Session) -> list[MeetingResult]:
    try:
        meeting_results = db.query(MeetingResult).filter(MeetingResult.meeting_id == meeting_id).all()

        if meeting_results:
            return meeting_results
        else:
            raise MeetingResultNotFound()
    except SQLAlchemyError:
        db.rollback()
        raise