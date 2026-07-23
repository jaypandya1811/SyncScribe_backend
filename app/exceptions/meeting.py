from .app_exception import AppError

class MeetingNotFound(AppError):
    status_code = 404
    error_code = "meeting_not_found"

    @property
    def default_message(self) -> str:
        return "No meetings found."


class MeetingUpdateError(AppError):
    status_code = 400
    error_code = "meeting_update_error"

    @property
    def default_message(self) -> str:
        return "Unable to update meeting."

class MeetingOverviewError(AppError):
    status_code = 400
    error_code = "meeting_overview_error"

    @property
    def default_message(self) -> str:
        return "Failed to fetch meeting overview"