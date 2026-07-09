from botocore.exceptions import ClientError
from urllib.parse import urlparse
from app.utils.s3_client import s3_client, BUCKET_NAME
from sqlalchemy.orm import Session
from app.repositories.meeting_audio_file.get_meeting_audio_file_by_id import get_meeting_audio_file_repo
from app.core.logger import logger

def extract_s3_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path.lstrip("/")

def build_audio_file_url_service(audio_file_id: int, db: Session) -> str:
    audio_file = get_meeting_audio_file_repo(audio_file_id=audio_file_id, db=db)

    key = extract_s3_url(audio_file.url) # type: ignore

    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=3600,
        )
    except ClientError as e:
        logger.error(f"s3 presigned url generation failed for id: {audio_file_id}: {e}")
        raise e
    return presigned_url