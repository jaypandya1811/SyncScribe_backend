from sqlalchemy.orm import Session
from app.repositories.meeting import get_meeting_repo
from app.db.models.meeting import Meeting
from app.core.logger import logger

def get_meeting_service(meeting_id: int, db: Session) -> Meeting:
    meeting_data = get_meeting_repo(meeting_id=meeting_id, db=db)
    logger.info(f"meeting by id:{meeting_data}")
    return meeting_data