from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.meetings import MeetingCreate, MeetingResponse, MeetingUpdate
from app.services.meeting import create_meeting_service, get_meeting_by_user_service, get_meeting_service, update_meeting_service

router = APIRouter(
    prefix="/meeting",
    tags=["Meetings"],
)

@router.post(
    "/create_meeting",
    response_model=MeetingResponse,
    status_code=status.HTTP_201_CREATED,
    )

def create_meeting(
    user_id: int = Form(...),
    name: str = Form(...),
    audio_url: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)):
    return create_meeting_service(user_id=user_id, name=name, audio_url=audio_url, file=file, db=db)

@router.get("/get_meetings/{user_id}", response_model=list[MeetingResponse], status_code=status.HTTP_200_OK)
def get_meetings_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_meeting_by_user_service(user_id=user_id, db=db)

@router.get("/{meeting_id}", response_model=MeetingResponse, status_code=status.HTTP_200_OK)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    return get_meeting_service(meeting_id=meeting_id, db=db)

@router.put("/update_meeting/{meeting_id}", response_model=MeetingResponse, status_code=status.HTTP_200_OK)
def update_meeting(meeting_id: int, meeting: MeetingUpdate, db: Session = Depends(get_db)):
    return update_meeting_service(meeting_id=meeting_id, meeting=meeting, db=db)