from sqlalchemy.orm import Session
from app.repositories.meeting_result import create_meeting_result_repo
from app.db.models.meeting_result import MeetingResult
from app.schema.meeting_results import MeetingResultCreate
from app.core.logger import logger

def create_meeting_result_service(meeting_result: MeetingResultCreate, db: Session) -> MeetingResult:
    meeting_result_data = create_meeting_result_repo(meeting_result=meeting_result, db=db)
    logger.info("meeting result created.")
    return meeting_result_data