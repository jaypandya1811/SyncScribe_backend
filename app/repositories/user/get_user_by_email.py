from sqlalchemy.orm import Session
from app.db.models.user import User
from sqlalchemy.exc import SQLAlchemyError

def get_user_by_email(db: Session, email: str) -> User | None:
    try: 
        user = db.query(User).filter(User.email == email).first()

        return user
    except SQLAlchemyError:
        db.rollback()
        raise