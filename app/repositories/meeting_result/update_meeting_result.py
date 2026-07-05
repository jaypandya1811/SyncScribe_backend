from sqlalchemy.orm import Session
from app.db.models.meeting_result import MeetingResult
from app.schema.meeting_results import MeetingResultUpdate
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.meeting_result import MeetingResultNotFound, MeetingResultUpdateError
from app.repositories.meeting_result.get_meeting_result_by_id import get_meeting_result_repo

def update_meeting_result_repo(meeting_result_id: int, meeting_result: MeetingResultUpdate, db: Session) -> MeetingResult:
    meeting_result_data = get_meeting_result_repo(meeting_result_id=meeting_result_id, db=db)
    if not meeting_result_data:
        raise MeetingResultNotFound()
    
    try:
        for key, value in meeting_result.model_dump(exclude_unset=True).items():
            setattr(meeting_result_data, key, value)
        db.commit()
        db.refresh(meeting_result_data)
        return meeting_result_data
    except SQLAlchemyError:
        db.rollback()
        raise MeetingResultUpdateError()