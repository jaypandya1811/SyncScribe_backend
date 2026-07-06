from app.exceptions.app_exception import AppError

class MeetingAudioFileNotFoundError(AppError):
    status_code = 404
    error_code = "meeting_audio_file_not_found"

    @property
    def default_message(self) -> str:
        return "No meeting audio file(s) found."