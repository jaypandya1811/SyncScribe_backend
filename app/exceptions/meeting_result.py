from .app_exception import AppError

class MeetingResultNotFound(AppError):
    status_code = 404
    error_code = "meeting_result_not_found"

    @property
    def default_message(self) -> str:
        return "No meeting results found."


class MeetingResultUpdateError(AppError):
    status_code = 400
    error_code = "meeting_result_update_error"

    @property
    def default_message(self) -> str:
        return "Unable to update meeting result."