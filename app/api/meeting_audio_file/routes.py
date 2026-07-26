from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.schema.users import UserResponse
from app.services.auth import AuthService
from typing import Optional
from app.db.models.meeting_audio import MeetingAudioFileStatus
from app.db.database import get_db
from app.schema.meeting_audio_file import MeetingAudioFileResponse
from app.services.meeting_audio_file import create_meeting_audio_file_service, get_meeting_audio_file_by_user_service, get_meeting_audio_file_by_meeting_service, get_meeting_audio_file_by_meeting_and_user_service, get_meeting_audio_file_service, update_meeting_audio_file_service, delete_meeting_audio_file_service
from app.services.audio_file_result import get_audio_result_service
import json

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
    meeting_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user_service)):
    return create_meeting_audio_file_service(user_id=current_user.id, meeting_id=meeting_id, file=file, db=db)

@router.get("/{audio_file_id}", response_model=MeetingAudioFileResponse, status_code=status.HTTP_200_OK)
def get_audio_file_by_id(audio_file_id: int, db: Session = Depends(get_db)):
    return get_meeting_audio_file_service(audio_file_id=audio_file_id, db=db)

@router.get(
    "/audio/user",
    response_model=list[MeetingAudioFileResponse],
    status_code=status.HTTP_200_OK,
    )

def get_meeting_audio_files_by_user_id(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user_service)):
    return get_meeting_audio_file_by_user_service(user_id=current_user.id, db=db)

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
    "/audio/user/meeting/{meeting_id}",
    response_model=list[MeetingAudioFileResponse],
    status_code=status.HTTP_200_OK,
    )

def get_meeting_audio_files_by_user_id_and_meeting_id(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user_service)):
    return get_meeting_audio_file_by_meeting_and_user_service(user_id=current_user.id, meeting_id=meeting_id,db=db)

@router.put("/audio/update/{audio_file_id}", response_model=MeetingAudioFileResponse, status_code=status.HTTP_200_OK)
def update_meeting_audio_file(
    id: int = Form(...),
    status: MeetingAudioFileStatus = Form(...),
    transcription: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    action_items: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    ):
    return update_meeting_audio_file_service(
        id=id,
        status=status,
        transcription=transcription,
        summary=summary,
        action_items=json.loads(action_items) if action_items else None,
        db=db,
        )

@router.get("/result/{audio_file_id}", response_model=MeetingAudioFileResponse, status_code=status.HTTP_200_OK)
def get_audio_file_result(audio_file_id: int, db: Session = Depends(get_db)):
    return get_audio_result_service(audio_file_id=audio_file_id, db=db)

@router.delete("/delete/{audio_file_id}", response_model=MeetingAudioFileResponse, status_code=status.HTTP_200_OK)
def delete_meeting_audio_file(audio_file_id: int, db: Session = Depends(get_db)):
    return delete_meeting_audio_file_service(audio_file_id=audio_file_id, db=db)