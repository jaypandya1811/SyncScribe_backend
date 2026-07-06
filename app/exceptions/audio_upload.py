from .app_exception import AppError

class AudioFileUploadError(AppError):
    status_code = 502
    error_code = "audio_file_upload_error"

    @property
    def default_message(self) -> str:
        return "Failed to upload audio file to aws."


class InvalidAudioFileExtensionError(AppError):
    status_code = 400
    error_code = "invalid_audio_file_extension"

    @property
    def default_message(self) -> str:
        return "Invalid file type."


class EmptyFileError(AppError):
    status_code = 400
    error_code = "empty_file"

    @property
    def default_message(self) -> str:
        return "Uploaded file is empty."


class FileSizeError(AppError):
    status_code = 413
    error_code = "file_size_exceeded"

    @property
    def default_message(self) -> str:
        return "Uploaded file size exceeds limit of 100 mb."


class InvalidFileTypeError(AppError):
    status_code = 400
    error_code = "invalid_file_type"

    @property
    def default_message(self) -> str:
        return "Invalid mime type."


class InvalidFileError(AppError):
    status_code = 400
    error_code = "invalid_file"

    @property
    def default_message(self) -> str:
        return "Invalid file."


class AudioDurationError(AppError):
    status_code = 400
    error_code = "audio_duration_error"

    @property
    def default_message(self) -> str:
        return "Uploaded audio file is too short to upload minimum 1 minute duration is required."


class AudioConverstionError(AppError):
    status_code = 500
    error_code = "audio_conversion_error"

    @property
    def default_message(self) -> str:
        return "Failed to convert video to audio."