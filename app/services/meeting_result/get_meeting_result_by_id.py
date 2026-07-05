from sqlalchemy.orm import Session
from app.repositories.meeting_result import get_meeting_result_repo
from app.db.models.meeting_result import MeetingResult
from app.core.logger import logger

def get_meeting_result_service(meeting_result_id: int, db: Session) -> MeetingResult:
    meeting_result_data = get_meeting_result_repo(meeting_result_id=meeting_result_id, db=db)
    logger.info(f"meeting result by id:{meeting_result_data}")
    return meeting_result_data