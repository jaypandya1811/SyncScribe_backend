from sqlalchemy.orm import Session
from app.repositories.meeting import delete_meeting_repo
from app.core.logger import logger

def delete_meeting_service(meeting_id: int, db: Session):
    meeting_data = delete_meeting_repo(meeting_id=meeting_id, db=db)
    logger.info(f"meeting deleted with id:{meeting_data}")