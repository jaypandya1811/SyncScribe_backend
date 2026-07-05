from fastapi import FastAPI
from app.db import Base, engine
from contextlib import asynccontextmanager
from .api.router import api_router
from .exceptions.handlers import user_already_exists_handler, user_not_found_handler, invalide_credentials_exception_handler, meeting_not_found_handler, meeting_update_error_handler, meeting_result_not_found_handler, meeting_result_update_error_handler, invalid_file_type_error_handler, empty_file_error_handler, file_extension_error_handler, file_size_error_handler, invalid_file_error_handler, file_duration_error_handler, audio_converstion_error_handler
from .exceptions.user import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError
from .exceptions.meeting import MeetingNotFound, MeetingUpdateError
from .exceptions.meeting_result import MeetingResultNotFound, MeetingResultUpdateError
from .exceptions.audio_upload import InvalidAudioFileExtensionError, InvalidFileTypeError, EmptyFileError, FileSizeError, InvalidFileError, AudioDurationError, AudioConverstionError

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Verifying database connectivity...")
    try:
        Base.metadata.create_all(bind=engine)
        with engine.connect() as connection:
            print("Successfully connected to the Supabase PostgreSQL instance!")
    except Exception as e:
        print(f"Database connection failed during startup: {e}")
        raise e
        
    yield
    
    print("Shutting down: Cleaning up database connection pool...")
    engine.dispose()
    print("Shutdown complete.")

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler,
)
app.add_exception_handler(
    UserNotFoundError,
    user_not_found_handler,
)

app.add_exception_handler(
    InvalidCredentialsError,
    invalide_credentials_exception_handler,
)

app.add_exception_handler(
    MeetingNotFound,
    meeting_not_found_handler,
)

app.add_exception_handler(
    MeetingUpdateError,
    meeting_update_error_handler,
)

app.add_exception_handler(
    MeetingResultNotFound,
    meeting_result_not_found_handler,
)

app.add_exception_handler(
    MeetingResultUpdateError,
    meeting_result_update_error_handler,
)

app.add_exception_handler(
    InvalidAudioFileExtensionError,
    file_extension_error_handler,
)

app.add_exception_handler(
    InvalidFileTypeError,
    invalid_file_type_error_handler,
)

app.add_exception_handler(
    EmptyFileError,
    empty_file_error_handler,
)

app.add_exception_handler(
    FileSizeError,
    file_size_error_handler,
)

app.add_exception_handler(
    InvalidFileError,
    file_size_error_handler,
)

app.add_exception_handler(
    AudioDurationError,
    file_size_error_handler,
)

app.add_exception_handler(
    AudioConverstionError,
    audio_converstion_error_handler,
)
