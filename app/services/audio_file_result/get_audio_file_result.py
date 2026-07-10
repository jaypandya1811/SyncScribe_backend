from app.services.audio_transcription import transcribe_audio_service
from app.repositories.meeting_audio_file.update_meeting_audio_file import update_meeting_audio_file_repo
from app.repositories.meeting_audio_file.get_meeting_audio_file_by_id import get_meeting_audio_file_repo
from app.services.audio_file_url.get_audio_file_url import build_audio_file_url_service
from app.exceptions.audio_file_result import AudioFileResultError
from app.exceptions.meeting_audio_file import MeetingAudioFileNotFoundError
from app.schema.meeting_audio_file import MeetingAudioFileUpdate
from app.db.models.meeting_audio import MeetingAudioFileStatus
from sqlalchemy.orm import Session
from app.schema.meeting_audio_file import MeetingAudioFileResponse
from app.core.logger import logger

def get_audio_result_service(audio_file_id: int, db: Session) -> MeetingAudioFileResponse:
    try:
        url = build_audio_file_url_service(audio_file_id=audio_file_id, db=db)
        transcription = transcribe_audio_service(url)
        meeting_audio_file_update = MeetingAudioFileUpdate(
            id= audio_file_id,
            status= MeetingAudioFileStatus.TRANSCRIBED,
            transcription= transcription.text,
        )
        updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
        return updated_data
    except MeetingAudioFileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"An error occured while generating audio file result: {e}")
        raise AudioFileResultError()
