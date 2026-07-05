from sqlalchemy.orm import Session
from app.db.models.user import User
from sqlalchemy.exc import SQLAlchemyError

def create_user(db: Session, email: str, password: str) -> User:
    try: 
        user = User(
            email=email,
            password=password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except SQLAlchemyError:
        db.rollback()
        raise