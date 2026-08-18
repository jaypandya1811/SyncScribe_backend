from collections import defaultdict
from sqlalchemy.orm import Session
from app.schema.meetings import MeetingOverviewResponse, AudioFileSummaryBlock
from app.core.logger import logger
from app.exceptions.meeting import MeetingNotFound, MeetingOverviewError
from app.repositories.meeting.get_meeting_by_user import get_meeting_by_user_repo
from app.repositories.meeting_audio_file.get_meeting_audio_files_by_meeting_ids import get_meeting_audio_fiels_by_meeting_ids_repo

def get_meeting_details_service(user_id: int, db: Session) -> list[MeetingOverviewResponse]:
    try:
        meetings = get_meeting_by_user_repo(user_id=user_id, db=db)
        meetings_id = [meeting.id for meeting in meetings]
        audio_files_db = get_meeting_audio_fiels_by_meeting_ids_repo(meeting_ids= meetings_id, db=db)

        audio_files_by_meeting_id: dict[int, list] = defaultdict(list)
        for audio_file in audio_files_db:
            audio_files_by_meeting_id[audio_file.meeting_id].append(audio_file)

        details = []
        for meeting in meetings:
            print(meeting)
            audio_files = []
            combined_action_items = []
            pending_count = 0
            meeting_audio_files = audio_files_by_meeting_id.get(meeting.id, [])

            for audio_file in meeting_audio_files:
                audio_files.append(AudioFileSummaryBlock(
                    audio_file_id= audio_file.id,
                    name= audio_file.original_filename,
                    url= audio_file.url,
                    status= audio_file.status,
                    summary= audio_file.summary,
                    action_items=None,
                    transcription= audio_file.transcription,
                    created_at= meeting.created_at,
                    updated_at= meeting.created_at,
                ))

                if audio_file.status != "summarized":
                    pending_count += 1
                    continue

                for item in (audio_file.action_items or []):
                    combined_action_items.append({
                        "task": item,
                        "audio_file_id": audio_file.id,
                    })

            logger.info(f"meeting details built for user_id: {user_id}, pending: {pending_count}")

            details.append(MeetingOverviewResponse(
                meeting_id= meeting.id,
                meeting_name= meeting.name,
                meeting_type= meeting.type,
                meeting_status= meeting.status,
                description= meeting.description,
                speakers= meeting.speakers,
                audio_files=audio_files,
                action_items=combined_action_items,
                pending_count=pending_count,
                action_items_count=len(combined_action_items),
                audio_file_count=len(meeting_audio_files),
                created_at= meeting.created_at,
            ))
        return details
    except MeetingNotFound:
        raise
    except Exception as e:
        logger.error(f"An error occurred while building meeting details: {e}")
        raise MeetingOverviewError()