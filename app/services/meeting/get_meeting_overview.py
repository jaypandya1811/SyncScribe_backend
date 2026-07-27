from sqlalchemy.orm import Session
from app.schema.meetings import MeetingOverviewResponse, AudioFileSummaryBlock
from app.core.logger import logger
from app.exceptions.meeting import MeetingNotFound, MeetingOverviewError
from app.repositories.meeting.get_meeting_by_id import get_meeting_repo
from app.repositories.meeting_audio_file.get_meeting_audio_file_by_meeting import get_meeting_audio_by_meeting_repo
from typing import cast
from datetime import datetime

def get_meeting_overview_service(meeting_id: int, db: Session) -> MeetingOverviewResponse:
    try:
        meeting = get_meeting_repo(meeting_id=meeting_id, db=db)
        audio_files_db = get_meeting_audio_by_meeting_repo(meeting_id=meeting_id, db=db)

        audio_files = []
        combined_action_items = []
        pending_count = 0
        audio_file_count = len(audio_files_db)

        if audio_file_count:
            for audio_file in audio_files_db:
                audio_files.append(AudioFileSummaryBlock(
                    audio_file_id=cast(int, audio_file.id),
                    name=cast(str, audio_file.original_filename),
                    url=cast(str, audio_file.url),
                    status=cast(str, audio_file.status),
                    summary=cast(str, audio_file.summary),
                    transcription=cast(str, audio_file.transcription),
                    created_at=cast(datetime, meeting.created_at),
                    updated_at=cast(datetime, meeting.created_at),
                ))

                if cast(str, audio_file.status) != "summarized":
                    pending_count += 1
                    continue

                for item in (audio_file.action_items or []):
                    combined_action_items.append({
                        **item,
                        "audio_file_id": audio_file.id,
                    })

        logger.info(f"meeting overview built for meeting_id: {meeting_id}, pending: {pending_count}")

        return MeetingOverviewResponse(
            meeting_id=meeting_id,
            meeting_name=cast(str, meeting.name),
            meeting_type=cast(str, meeting.type),
            meeting_status=cast(str, meeting.status),
            speakers=cast(int, meeting.speakers),
            audio_files=audio_files,
            action_items=combined_action_items,
            pending_count=pending_count,
            action_items_count=len(combined_action_items),
            audio_file_count=audio_file_count,
            created_at=cast(datetime, meeting.created_at),
        )
    except MeetingNotFound:
        raise
    except Exception as e:
        logger.error(f"An error occurred while building meeting overview: {e}")
        print(e)
        raise MeetingOverviewError()