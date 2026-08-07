from sqlalchemy.orm import Session
from app.repositories.meeting import update_meeting_repo
from app.db.models.meeting import Meeting
from app.schema.meetings import MeetingUpdate
from app.core.logger import logger

def update_meeting_service(meeting_id: int, meeting: MeetingUpdate, db: Session) -> Meeting:
    meeting_data = update_meeting_repo(meeting_id=meeting_id, meeting=meeting, db=db)
    logger.info(f"meeting data updated: {meeting_data}")
    return meeting_data