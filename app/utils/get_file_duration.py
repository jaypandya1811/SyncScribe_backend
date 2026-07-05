from mutagen import File as mfile
import io
from app.exceptions.audio_upload import InvalidFileError

def get_file_duration(file_bytes: bytes) -> float:
    audio = mfile(io.BytesIO(file_bytes))
    if audio is None or audio.info is None:
        raise InvalidFileError()
    return audio.info.length