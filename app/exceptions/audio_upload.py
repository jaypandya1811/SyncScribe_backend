class AudioFileUploadError(Exception):

    def __init__(self):

        super().__init__("Failed to upload audio file to aws.")

class InvalidAudioFileExtensionError(Exception):

    def __init__(self):

        super().__init__("Invalid file type.")

class EmptyFileError(Exception):

    def __init__(self):

        super().__init__("Uploaded file is empty.")

class FileSizeError(Exception):

    def __init__(self):

        super().__init__("Uploaded file size exceeds limit of 100 mb.")

class InvalidFileTypeError(Exception):

    def __init__(self):

        super().__init__("Invalid mime type.")

class InvalidFileError(Exception):

    def __init__(self):

        super().__init__("Invalid file.")

class AudioDurationError(Exception):

    def __init__(self):

        super().__init__("Uploaded audio file is too short to upload minimum 1 minute duration is required.")

class AudioConverstionError(Exception):

    def __init__(self):

        super().__init__("Failed to convert video to audio.")