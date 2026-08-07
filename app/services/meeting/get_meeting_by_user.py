from sqlalchemy.orm import Session
from app.repositories.meeting import get_meeting_by_user_repo
from app.db.models.meeting import Meeting
from app.core.logger import logger

def get_meeting_by_user_service(user_id: int, db: Session) -> list[Meeting]:
    meeting_data = get_meeting_by_user_repo(user_id=user_id, db=db)
    logger.info(f"meetings by user id:{meeting_data}")
    return meeting_data