import uuid
import io
from fastapi import UploadFile
from app.utils.s3_client import s3_client, BUCKET_NAME
from botocore.exceptions import BotoCoreError, ClientError
from app.exceptions import AudioFileUploadError, InvalidFileError
from app.core.logger import logger
from app.utils.validate_file import validate_file
from app.utils.video_to_audio import extract_audio_from_video

CONTENT_TYPE_MAP = {
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "m4a": "audio/mp4",
    "ogg": "audio/ogg",
    "webm": "audio/webm",
}

VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv"}

def get_content_type(file_extension: str) -> str:
    return CONTENT_TYPE_MAP.get(file_extension, "application/octet-stream")

def upload_audio_to_s3(file: UploadFile, user_id: int, meeting_id: int) -> str:
    file_name = file.filename
    if not file_name:
        raise InvalidFileError()
    file_extension = file_name.rsplit(".")[-1].lower()
    try:
        file_bytes = file.file.read()
        file.file.seek(0)

        if file_extension in VIDEO_EXTENSIONS:
            file_bytes, file_extension = extract_audio_from_video(
                    video_bytes=file_bytes, video_extension=file_extension
                )

        validate_file(file_name, file_bytes, file_extension)

        unique_filename = f"audio/{user_id}/{meeting_id}/{uuid.uuid4()}.{file_extension}"

        content_type = get_content_type(file_extension)

        s3_client.upload_fileobj(
            io.BytesIO(file_bytes),
            BUCKET_NAME,
            unique_filename,
            ExtraArgs={"ContentType": content_type},
        )

        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

        logger.info(f"audio file uploaded to s3 upload url: {file_url}")

        return file_url
    except (ClientError, BotoCoreError) as e:
        logger.error(f"something went wrong while uploading audio file to s3, error: {e}")
        raise AudioFileUploadError