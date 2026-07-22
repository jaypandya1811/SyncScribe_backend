from sqlalchemy.orm import Session
from app.db.models.user import User
from sqlalchemy.exc import SQLAlchemyError

def create_user(db: Session, first_name: str, last_name: str,email: str, password: str) -> User:
    try: 
        user = User(
            first_name=first_name,
            last_name=last_name,
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