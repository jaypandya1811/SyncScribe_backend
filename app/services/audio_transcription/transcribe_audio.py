import os
import requests
from app.exceptions.transcription_exception import TranscriptionFailed
from app.utils.groq_client import groq_client
from app.schema.ai_schema import TranscriptionResult
from dotenv import load_dotenv
from typing import cast
from app.core.logger import logger

load_dotenv()

model = cast(str, os.getenv("TRANSCRIPTION_MODEL"))

def transcribe_audio_service(file_url: str) -> TranscriptionResult:
    try:
        response = requests.get(file_url, timeout=30)
        response.raise_for_status()
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.m4a", response.content),
            model=model,
            language="en",
            response_format="verbose_json",
        )
        return TranscriptionResult(
            text=transcription.text,
            segments=getattr(transcription, "segments", []) or [],
        )
    except Exception as e:
        logger.error(f"An error occured while transcribing an audio: ", {e})
        raise TranscriptionFailed()