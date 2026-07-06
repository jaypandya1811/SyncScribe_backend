from fastapi import APIRouter
from .user.routes import router as user_router
from .meeting.routes import router as meeting_router 
from .meeting_result.routes import router as meeting_result_router
from .meeting_audio_file.routes import router as meeting_audio_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(meeting_router)
api_router.include_router(meeting_result_router)
api_router.include_router(meeting_audio_router)