from app.exceptions.app_exception import AppError

class AudioFileResultError(AppError):
    status_code = 502
    error_code = "audio_file_result_error"

    @property
    def default_message(self) -> str:
        return "Failed to generate audio file result."

class RetryLimitError(AppError):
    status_code = 502
    error_code = "audio_file_result_error"

    @property
    def default_message(self) -> str:
        return "Retry limit for this audio file is exceeded."