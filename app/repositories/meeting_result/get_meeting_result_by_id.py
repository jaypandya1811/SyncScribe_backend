from sqlalchemy.orm import Session
from app.db.models.meeting_result import MeetingResult
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_result import MeetingResultNotFound

def get_meeting_result_repo(meeting_result_id: int, db: Session) -> MeetingResult:
    try:
        meeting_result = db.get(MeetingResult, meeting_result_id)

        if meeting_result:
            return meeting_result
        else:
            raise MeetingResultNotFound()
    except SQLAlchemyError:
        db.rollback()
        raise