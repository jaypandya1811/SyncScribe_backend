import subprocess
import tempfile
import os
from app.core.logger import logger
from app.exceptions.audio_upload import AudioConverstionError

def extract_audio_from_video(video_bytes: bytes, video_extension: str) -> tuple[bytes, str]:
    FFMPEG_PATH = r"C:\Program Files\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, f"input.{video_extension}")
        output_path = os.path.join(temp_dir, "output.m4a")

        with open(input_path, "wb") as f:
            f.write(video_bytes)

        try:
            subprocess.run(
                [
                    FFMPEG_PATH,
                    "-i", input_path,
                    "-vn",
                    "-acodec", "copy",
                    output_path,
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"video to audio conversion failed error: {e.stderr.decode()}")
            raise AudioConverstionError()

        with open(output_path, "rb") as f:
            audio_bytes = f.read()

        return audio_bytes, "m4a"