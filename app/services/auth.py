from sqlalchemy.orm import Session
from fastapi import Response, Request
from app.repositories.user import create_user, get_user_by_email
from app.schema.users import UserCreate, UserLogin
from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError
from app.utils import hash_password, verify_password
from app.core.logger import logger
from app.core.config import settings
from app.core.security import create_access_token, decode_access_token
from app.exceptions.user import NotAuthenticatedError, InvalidTokenError
from app.repositories.user import get_user_by_id_repo

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
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password
        )

        logger.info("user created successfully")

        return userData

    @staticmethod
    def login(
        db: Session,
        response: Response,
        user: UserLogin,
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

        token = create_access_token(data={"sub": str(user_by_email.id)})

        print(f"generated token for user: {token}")

        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )
        return user_by_email

    @staticmethod
    def get_current_user_service(request: Request, db: Session):
        token = request.cookies.get(settings.COOKIE_NAME)
        if not token:
            raise NotAuthenticatedError()

        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            raise InvalidTokenError()

        user_id = int(payload["sub"])
        db_user = get_user_by_id_repo(id=user_id, db=db)
        if not db_user:
            raise InvalidTokenError()

        return db_user