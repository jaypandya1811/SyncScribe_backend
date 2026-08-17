import magic
from app.exceptions.audio_upload import InvalidAudioFileExtensionError, InvalidFileTypeError, FileSizeError,EmptyFileError, AudioDurationError
from app.utils.get_file_duration import get_file_duration

ALLOWED_EXTENSIONS = {
    "mp3",
    "mpeg",
    "wav",
    "m4a",
    "mp4",
    "webm",
    "ogg",
    "aac",
    "flac",
    "amr",
    "3gp",
}
ALLOWED_MIME_TYPES = {
    "audio/mpeg",
    "video/mpeg",  
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",       
    "audio/x-m4a",
    "audio/aac",
    "audio/x-aac",
    "audio/flac",
    "audio/x-flac",
    "audio/amr",
    "audio/3gpp",     
    "video/3gpp",
    "audio/webm",
    "video/webm",
    "audio/ogg",
    "application/ogg",
}
MAX_FILE_SIZE = 100 * 1024 * 1024
MIN_DURATION_SECONDS = 60

def validate_file(file_name: str, file_bytes: bytes, file_extension: str) -> None:
    if "." not in file_name:
        raise InvalidAudioFileExtensionError()

    file_extension = file_name.rsplit(".", 1)[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise InvalidAudioFileExtensionError()
    
    file_size = len(file_bytes)
    if file_size == 0:
        raise EmptyFileError()
    if file_size > MAX_FILE_SIZE:
        raise FileSizeError()

    detected_mime = magic.from_buffer(file_bytes, mime=True)
    if detected_mime not in ALLOWED_MIME_TYPES:
        raise InvalidFileTypeError()
    
    duration = get_file_duration(file_bytes, file_name)

    if duration < MIN_DURATION_SECONDS:
        raise AudioDurationError()