from app.exceptions.app_exception import AppError

class TranscriptionFailed(AppError):
    status_code = 502
    error_code = "transcription_failed"

    @property
    def default_message(self) -> str:
        return "Failed to transcribe audio."