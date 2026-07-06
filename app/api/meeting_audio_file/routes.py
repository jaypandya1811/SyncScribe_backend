from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.meeting_audio_file import MeetingAudioFileCreate, MeetingAudioFileResponse
from app.services.meeting_audio_file import create_meeting_audio_file_service, get_meeting_audio_file_by_user_service, get_meeting_audio_file_by_meeting_service, get_meeting_audio_file_by_meeting_and_user_service

router = APIRouter(
    prefix="/uploads",
    tags=["Meeting audio file"],
)

@router.post(
    "/audio",
    response_model=MeetingAudioFileResponse,
    status_code=status.HTTP_201_CREATED,
    )

def create_meeting_audio_file(
    user_id: int = Form(...),
    meeting_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)):
    return create_meeting_audio_file_service(user_id=user_id, meeting_id=meeting_id, file=file, db=db)

@router.get(
    "/audio/user/{user_id}",
    response_model=list[MeetingAudioFileResponse],
    status_code=status.HTTP_200_OK,
    )

def get_meeting_audio_files_by_user_id(
    user_id: int,
    db: Session = Depends(get_db)):
    return get_meeting_audio_file_by_user_service(user_id=user_id, db=db)

@router.get(
    "/audio/meeting/{meeting_id}",
    response_model=list[MeetingAudioFileResponse],
    status_code=status.HTTP_200_OK,
    )

def get_meeting_audio_files_by_meeting_id(
    meeting_id: int,
    db: Session = Depends(get_db)):
    return get_meeting_audio_file_by_meeting_service(meeting_id=meeting_id, db=db)

@router.get(
    "/audio/user/{user_id}/meeting/{meeting_id}",
    response_model=list[MeetingAudioFileResponse],
    status_code=status.HTTP_200_OK,
    )

def get_meeting_audio_files_by_user_id_and_meeting_id(
    user_id: int,
    meeting_id: int,
    db: Session = Depends(get_db)):
    return get_meeting_audio_file_by_meeting_and_user_service(user_id=user_id, meeting_id=meeting_id,db=db)