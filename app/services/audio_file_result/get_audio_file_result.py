from app.services.audio_transcription import transcribe_audio_service
from app.services.summarize_audio import summarize_audio_service
from app.services.meeting_audio_file.get_meeting_audio_file_by_id import get_meeting_audio_file_repo
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
        audio_file = get_meeting_audio_file_repo(audio_file_id=audio_file_id, db=db)
        updated_data = None
        current_status = audio_file.status
        if current_status == "uploaded" or current_status == "transcript_failed": # type: ignore
            url = build_audio_file_url_service(audio_file_id=audio_file_id, db=db)
            transcription = transcribe_audio_service(url)
            if not transcription.text:
                meeting_audio_file_update = MeetingAudioFileUpdate(
                id= audio_file_id,
                status= MeetingAudioFileStatus.TRANSCRIPT_FAILED,
                )   
                logger.error(f"transcription failed for audio file with id: {audio_file_id}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
                return updated_data
            else:
                meeting_audio_file_update = MeetingAudioFileUpdate(
                    id= audio_file_id,
                    status= MeetingAudioFileStatus.TRANSCRIBED,
                    transcription= transcription.text,
                )
                logger.info(f"transcription generated for audio file with id: {audio_file_id}, transcrption: {transcription.text}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
                current_status = updated_data.status
        if current_status == "transcribed" or current_status == "summarization_failed": # type: ignore
            summary = summarize_audio_service(audio_file.transcription) # type: ignore
            if not summary:
                meeting_audio_file_update = MeetingAudioFileUpdate(
                id= audio_file_id,
                status= MeetingAudioFileStatus.SUMMARIZATION_FAILED,
                ) 
                logger.error(f"summarization failed for audio file with id: {audio_file_id}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
                return updated_data
            else:     
                meeting_audio_file_update = MeetingAudioFileUpdate(
                    id= audio_file_id,
                    status= MeetingAudioFileStatus.SUMMARIZED,
                    summary=summary.summary,
                    action_items=[item.model_dump() for item in summary.action_items],
                )
                logger.info(f"summary and action items generated for audio file with id: {audio_file_id}, summary: {summary}, action items: {[item.model_dump() for item in summary.action_items]}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
            if updated_data is None:
                logger.error(f"Unexpected audio file status: {audio_file.status} for id: {audio_file_id}")
                raise AudioFileResultError()
        return updated_data
    except MeetingAudioFileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"An error occured while generating audio file result: {e}")
        raise AudioFileResultError()
