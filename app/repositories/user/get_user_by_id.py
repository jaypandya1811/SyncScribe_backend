from sqlalchemy.orm import Session
from app.db.models.user import User
from sqlalchemy.exc import SQLAlchemyError

def get_user_by_id(db: Session, id: int) -> User | None:
    try: 
        user = db.get(User, id)

        return user
    except SQLAlchemyError:
        db.rollback()
        raise