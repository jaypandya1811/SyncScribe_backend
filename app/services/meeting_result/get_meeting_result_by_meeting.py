from sqlalchemy.orm import Session
from app.repositories.meeting_result import get_meeting_result_by_meeting_repo
from app.db.models.meeting_result import MeetingResult
from app.schema.meeting_results import MeetingResultCreate
from app.core.logger import logger

def get_meeting_result_by_meeting_service(meeting_id: int, db: Session) -> list[MeetingResult]:
    meeting_result_data = get_meeting_result_by_meeting_repo(meeting_id=meeting_id, db=db)
    logger.info(f"meeting results by meeting id:{meeting_result_data}")
    return meeting_result_data