from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.db.models.meeting import Meeting, MeetingStatus
from app.db.models.meeting_audio import MeetingAudioFile, MeetingAudioFileStatus
from app.schema.users import DashboardCounts
from sqlalchemy.exc import SQLAlchemyError

def get_dashboard_counts_repo(db: Session, user_id: int) -> DashboardCounts:
    try: 
        meeting_count = (
            db.query(func.count(Meeting.id))
            .filter(Meeting.user_id == user_id)
            .scalar()
        )
        pending_meeting_count = (
            db.query(func.count(Meeting.id))
            .filter(Meeting.user_id == user_id, Meeting.status == MeetingStatus.PENDING)
            .scalar()
        )
        audio_file_count = (
            db.query(func.count(MeetingAudioFile.id))
            .filter(MeetingAudioFile.user_id == user_id)
            .scalar()
        )
        failed_audio_file_count = (
            db.query(func.count(MeetingAudioFile.id))
            .filter(
            MeetingAudioFile.user_id == user_id,
            or_(
                MeetingAudioFile.status == MeetingAudioFileStatus.TRANSCRIPT_FAILED,
                MeetingAudioFile.status == MeetingAudioFileStatus.SUMMARIZATION_FAILED,
            ),
            )
            .scalar()
        )
        counts = DashboardCounts(
            meeting_count=meeting_count,
            pending_meeting_count=pending_meeting_count,
            audio_file_count=audio_file_count,
            failed_audiofile_count=failed_audio_file_count,
        )
        return counts
    except SQLAlchemyError:
        db.rollback()
        raise