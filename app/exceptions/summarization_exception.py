from app.exceptions.app_exception import AppError

class SummarizationFailed(AppError):
    status_code = 502
    error_code = "summarization_failed"

    @property
    def default_message(self) -> str:
        return "Failed to generate summary/action items."