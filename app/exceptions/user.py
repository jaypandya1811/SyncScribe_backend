from .app_exception import AppError

class UserAlreadyExistsError(AppError):
    status_code = 409
    error_code = "user_already_exists"

    @property
    def default_message(self) -> str:
        return "This email is already registered."

class UserNotFoundError(AppError):
    status_code = 404
    error_code = "user_not_found"

    @property
    def default_message(self) -> str:
        return "User not found."
        
class InvalidCredentialsError(AppError):
    status_code = 401
    error_code = "invalid_credentials"

    @property
    def default_message(self) -> str:
        return "Incorrect email or password."