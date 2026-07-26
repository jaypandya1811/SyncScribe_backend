from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.meetings import MeetingCreate, MeetingResponse, MeetingUpdate, MeetingOverviewResponse
from app.services.meeting import create_meeting_service, get_meeting_by_user_service, get_meeting_service, update_meeting_service, delete_meeting_service, get_meeting_overview_service
from app.services.auth import AuthService
from app.schema.users import UserResponse

router = APIRouter(
    prefix="/meeting",
    tags=["Meetings"],
)

@router.post(
    "/create_meeting",
    response_model=MeetingResponse,
    status_code=status.HTTP_201_CREATED,
    )

def create_meeting(meeting: MeetingCreate, current_user: UserResponse = Depends(AuthService.get_current_user_service),db: Session = Depends(get_db)):
    return create_meeting_service(user_id=current_user.id, name=meeting.name, type=meeting.type, description=meeting.description, speakers=meeting.speakers, db=db)

@router.get("/get_meetings", response_model=list[MeetingResponse], status_code=status.HTTP_200_OK)
def get_meetings_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_meeting_by_user_service(user_id=user_id, db=db)

@router.get("/{meeting_id}", response_model=MeetingResponse, status_code=status.HTTP_200_OK)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    return get_meeting_service(meeting_id=meeting_id, db=db)

@router.get("/overview/{meeting_id}", response_model=MeetingOverviewResponse, status_code=status.HTTP_200_OK)
def get_meeting_overview(meeting_id: int, db: Session = Depends(get_db)):
    return get_meeting_overview_service(meeting_id=meeting_id, db=db)

@router.put("/update_meeting/{meeting_id}", response_model=MeetingResponse, status_code=status.HTTP_200_OK)
def update_meeting(meeting_id: int, meeting: MeetingUpdate, db: Session = Depends(get_db)):
    return update_meeting_service(meeting_id=meeting_id, meeting=meeting, db=db)

@router.delete("/delete/{meeting_id}", response_model=MeetingResponse, status_code=status.HTTP_200_OK)
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    return delete_meeting_service(meeting_id=meeting_id, db=db)