from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.meeting_results import MeetingResultCreate, MeetingResultResponse, MeetingResultUpdate
from app.services.meeting_result import create_meeting_result_service, get_meeting_result_service, get_meeting_result_by_meeting_service, update_meeting_result_service

router = APIRouter(
    prefix="/meeting_results",
    tags=["Meeting results"],
)

@router.post("/create_meeting_result", response_model=MeetingResultResponse, status_code=status.HTTP_201_CREATED)
def create_meeting_result(meeting_result: MeetingResultCreate, db: Session = Depends(get_db)):
    return create_meeting_result_service(meeting_result=meeting_result, db=db)

@router.get("/{meeting_result_id}", response_model=MeetingResultResponse, status_code=status.HTTP_200_OK)
def get_meeting_result(meeting_result_id: int, db: Session = Depends(get_db)):
    return get_meeting_result_service(meeting_result_id=meeting_result_id, db=db)

@router.get("/get_meeting_results/{meeting_id}", response_model=list[MeetingResultResponse], status_code=status.HTTP_200_OK)
def get_meeting_result_by_meeting(meeting_id: int, db: Session = Depends(get_db)):
    return get_meeting_result_by_meeting_service(meeting_id=meeting_id, db=db)

@router.put("/update_meeting_result/{meeting_result_id}", response_model=MeetingResultResponse, status_code=status.HTTP_200_OK)
def update_meeting_result(meeting_result_id: int, meeting_result: MeetingResultUpdate, db: Session = Depends(get_db)):
    return update_meeting_result_service(meeting_result_id=meeting_result_id, meeting_result=meeting_result, db=db)