from sqlalchemy.orm import Session
from app.repositories.user import create_user, get_user_by_email
from app.schema.users import UserCreate, UserResponse
from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError
from app.utils import hash_password, verify_password
from app.core.logger import logger

class AuthService: 

    @staticmethod
    def register(
        db: Session,
        user: UserCreate
    ):
        is_exist = get_user_by_email(
            db=db,
            email=user.email
        )

        if is_exist:
            logger.error(f"user with email {user.email} is already exist")
            raise UserAlreadyExistsError()

        hashed_password = hash_password(
            user.password
        )

        userData = create_user(
            db=db,
            email=user.email,
            password=hashed_password
        )

        logger.info("user created successfully")

        return userData

    @staticmethod
    def login(
        db: Session,
        user: UserCreate,
    ):
        user_by_email = get_user_by_email(
            db=db,
            email=user.email
        )

        if user_by_email is None:
            logger.error(f"User with email {user.email} does not exist.")
            raise UserNotFoundError()

        if not verify_password(user.password, str(user_by_email.password)):
            raise InvalidCredentialsError()

        return user_by_email