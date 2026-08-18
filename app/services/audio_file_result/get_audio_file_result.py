from app.services.audio_transcription import transcribe_audio_service
from app.services.summarize_audio import summarize_audio_service
from app.services.meeting_audio_file.get_meeting_audio_file_by_id import get_meeting_audio_file_repo
from app.repositories.meeting_audio_file.update_meeting_audio_file import update_meeting_audio_file_repo
from app.repositories.meeting_audio_file.get_meeting_audio_file_by_id import get_meeting_audio_file_repo
from app.repositories.meeting.update_meeting import update_meeting_repo
from app.services.audio_file_url.get_audio_file_url import build_audio_file_url_service
from app.exceptions.audio_file_result import AudioFileResultError
from app.exceptions.meeting_audio_file import MeetingAudioFileNotFoundError
from app.exceptions.audio_file_result import RetryLimitError
from app.schema.meeting_audio_file import MeetingAudioFileUpdate
from app.db.models.meeting_audio import MeetingAudioFileStatus
from sqlalchemy.orm import Session
from app.schema.meeting_audio_file import MeetingAudioFileResponse
from app.schema.meetings import MeetingUpdate
from app.db.models.meeting import MeetingStatus
from app.core.logger import logger

def get_audio_result_service(audio_file_id: int, db: Session) -> MeetingAudioFileResponse:
    audio_file = get_meeting_audio_file_repo(audio_file_id=audio_file_id, db=db)
    retry_count = audio_file.retry_count or 0
    if retry_count >= 3:
        raise RetryLimitError()
    try:
        updated_data = None
        current_status = audio_file.status
        meeting_audio_file_update = MeetingAudioFileUpdate(
            id=audio_file_id,
            status= MeetingAudioFileStatus.PROCESSING,
        )
        update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
        meeting_update = MeetingUpdate(
            status= MeetingStatus.PROCESSING
        )
        update_meeting_repo(meeting_id=audio_file.meeting_id, meeting=meeting_update, db=db)
        if current_status == MeetingAudioFileStatus.TRANSCRIPT_FAILED or current_status == MeetingAudioFileStatus.SUMMARIZATION_FAILED: retry_count += 1
        if current_status == MeetingAudioFileStatus.UPLOADED or current_status == MeetingAudioFileStatus.TRANSCRIPT_FAILED or current_status == MeetingAudioFileStatus.PROCESSING:
            url = build_audio_file_url_service(audio_file_id=audio_file_id, db=db)
            transcription = transcribe_audio_service(url)
            if transcription is None or not transcription.text:
                meeting_audio_file_update = MeetingAudioFileUpdate(
                    id=audio_file_id,
                    status= MeetingAudioFileStatus.TRANSCRIPT_FAILED,
                    retry_count= retry_count,
                )  
                meeting_update = MeetingUpdate(
                    status= MeetingStatus.FAILED
                )
                logger.error(f"transcription failed for audio file with id: {audio_file_id}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
                update_meeting_repo(meeting_id=updated_data.meeting_id, meeting=meeting_update, db=db)
                return updated_data
            else:
                meeting_audio_file_update = MeetingAudioFileUpdate(
                    id=audio_file_id,
                    status= MeetingAudioFileStatus.TRANSCRIBED,
                    transcription= transcription.text,
                    retry_count= retry_count,
                )
                logger.info(f"transcription generated for audio file with id: {audio_file_id}, transcrption: {transcription.text}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
                print(f"updated audio file data in transcribe block", updated_data)
                current_status = updated_data.status
        if current_status == MeetingAudioFileStatus.TRANSCRIBED or current_status == MeetingAudioFileStatus.SUMMARIZATION_FAILED:
            summary = summarize_audio_service(audio_file.transcription) # type: ignore
            if not summary:
                meeting_audio_file_update = MeetingAudioFileUpdate(
                id= audio_file_id,
                status= MeetingAudioFileStatus.SUMMARIZATION_FAILED,
                retry_count= retry_count,
                ) 
                meeting_update = MeetingUpdate(
                    status= MeetingStatus.FAILED
                )
                logger.error(f"summarization failed for audio file with id: {audio_file_id}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
                update_meeting_repo(meeting_id=updated_data.meeting_id, meeting=meeting_update, db=db)
                return updated_data
            else:     
                meeting_audio_file_update = MeetingAudioFileUpdate(
                    id= audio_file_id,
                    status= MeetingAudioFileStatus.SUMMARIZED,
                    summary=summary.summary,
                    action_items=summary.action_items,
                    retry_count= retry_count,
                )
                meeting_update = MeetingUpdate(
                    status= MeetingStatus.COMPLETED
                )
                logger.info(f"summary and action items generated for audio file with id: {audio_file_id}, summary: {summary}, action items: {[summary.action_items]}")
                updated_data = update_meeting_audio_file_repo(audio_file_id=audio_file_id, meeting_audio_file_update=meeting_audio_file_update, db=db)
                print(f"updated audio file data in summarize block", updated_data)
                update_meeting_repo(meeting_id=updated_data.meeting_id, meeting=meeting_update, db=db)
            if updated_data is None:
                meeting_update = MeetingUpdate(
                    status= MeetingStatus.FAILED
                )
                update_meeting_repo(meeting_id=updated_data.meeting_id, meeting=meeting_update, db=db)
                logger.error(f"Unexpected audio file status: {audio_file.status} for id: {audio_file_id}")
                raise AudioFileResultError()
        return updated_data
    except MeetingAudioFileNotFoundError:
        raise
    except Exception as e:
        meeting_update = MeetingUpdate(
            status= MeetingStatus.FAILED
        )
        update_meeting_repo(meeting_id=audio_file.meeting_id, meeting=meeting_update, db=db)
        logger.error(f"An error occured while generating audio file result: {e}")
        raise AudioFileResultError()
