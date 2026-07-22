from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.users import UserCreate, UserResponse, UserLogin
from app.services.auth import AuthService
from app.services.user.get_userById import fetch_user_by_id

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    )

def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return AuthService.register(
        db=db,
        user=user,
    )

@router.post(
    "/login",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    )

def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return AuthService.login(
        db=db,
        user=user,
    )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    )

def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    return fetch_user_by_id(
        db=db,
        user_id=user_id,
    )