from sqlalchemy.orm import Session
from app.schema.meetings import MeetingOverviewResponse, AudioFileSummaryBlock
from app.core.logger import logger
from app.exceptions.meeting import MeetingNotFound, MeetingOverviewError
from app.repositories.meeting.get_meeting_by_id import get_meeting_repo
from app.repositories.meeting_audio_file.get_meeting_audio_file_by_meeting import get_meeting_audio_by_meeting_repo
from typing import cast

def get_meeting_overview_service(meeting_id: int, db: Session) -> MeetingOverviewResponse:
    try:
        meeting = get_meeting_repo(meeting_id=meeting_id, db=db)
        audio_files = get_meeting_audio_by_meeting_repo(meeting_id=meeting_id, db=db)

        summaries = []
        combined_action_items = []
        pending_count = 0

        for audio_file in audio_files:
            summaries.append(AudioFileSummaryBlock(
                audio_file_id=cast(int, audio_file.id),
                name=cast(str, audio_file.original_filename),
                status=cast(str, audio_file.status),
                summary=cast(str, audio_file.summary),
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
            summaries=summaries,
            action_items=combined_action_items,
            pending_count=pending_count,
        )
    except MeetingNotFound:
        raise
    except Exception as e:
        logger.error(f"An error occurred while building meeting overview: {e}")
        raise MeetingOverviewError()