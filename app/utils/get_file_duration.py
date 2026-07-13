import os
import json
import subprocess
import tempfile
from app.exceptions.audio_upload import InvalidFileError
from app.core.logger import logger

TEMP_DIR = os.path.join(os.getcwd(), "tmp_audio")
os.makedirs(TEMP_DIR, exist_ok=True)

def get_file_duration(file_bytes: bytes, file_name: str) -> float:
    ext = os.path.splitext(file_name)[1] or ".tmp"
    tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False, dir=TEMP_DIR)
    try:
        tmp.write(file_bytes)
        tmp.flush()
        tmp.close()
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                tmp.name,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except (subprocess.CalledProcessError, KeyError, ValueError, json.JSONDecodeError) as e:
        logger.error(f"failed to get file duration error: {e}")
        raise InvalidFileError()
    finally:
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)