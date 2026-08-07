import os
from pathlib import Path
from urllib.parse import urlparse
import requests
from app.utils.groq_client import groq_client
from app.schema.ai_schema import TranscriptionResult
from dotenv import load_dotenv
from typing import Optional, cast
from app.core.logger import logger

load_dotenv()

model = cast(str, os.getenv("TRANSCRIPTION_MODEL"))

def transcribe_audio_service(file_url: str) -> Optional[TranscriptionResult]:
    ext = Path(urlparse(file_url).path).suffix or ".m4a"
    try:
        response = requests.get(file_url, timeout=30)
        response.raise_for_status()
        transcription = groq_client.audio.transcriptions.create(
            file=(f"audio{ext}", response.content),
            model=model,
            language="en",
            response_format="verbose_json",
        )
        return TranscriptionResult(
            text=transcription.text,
            segments=getattr(transcription, "segments", []) or [],
        )
    except requests.RequestException as e:
        logger.error(f"failed to download audio file from {file_url}: {e}")
        return None
    except Exception as e:
        logger.error(f"groq transcription failed: {e}")
        return None