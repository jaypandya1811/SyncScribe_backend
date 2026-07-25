from sqlalchemy.orm import Session
from app.repositories.user import get_user_by_id_repo
from app.exceptions.user import UserNotFoundError
from app.core.logger import logger

def fetch_user_by_id(db: Session, user_id: int):
    user = get_user_by_id_repo(db, user_id)
    if user is None:
        logger.error(f"user not found with id: {user_id}")
        raise UserNotFoundError()
    return user