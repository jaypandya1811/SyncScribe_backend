class UserAlreadyExistsError(Exception):

    def __init__(self):

        super().__init__("This email is already registered.")

class UserNotFoundError(Exception):

    def __init__(self):

        super().__init__("User not found.")
        
class InvalidCredentialsError(Exception):

    def __init__(self):

        super().__init__("Incorrect email or password.")