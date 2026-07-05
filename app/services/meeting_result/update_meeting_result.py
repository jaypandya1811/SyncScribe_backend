from sqlalchemy.orm import Session
from app.repositories.meeting_result import update_meeting_result_repo
from app.db.models.meeting_result import MeetingResult
from app.schema.meeting_results import MeetingResultUpdate
from app.core.logger import logger

def update_meeting_result_service(meeting_result_id: int, meeting_result: MeetingResultUpdate, db: Session) -> MeetingResult:
    meeting_result_data = update_meeting_result_repo(meeting_result_id=meeting_result_id, meeting_result=meeting_result, db=db)
    logger.info(f"meeting result data updated: {meeting_result_data}")
    return meeting_result_data