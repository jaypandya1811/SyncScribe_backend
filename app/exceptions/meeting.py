class MeetingNotFound(Exception):

    def __init__(self):

        super().__init__("No meetings found.")

class MeetingUpdateError(Exception):

    def __init__(self):

        super().__init__("Unable to update meeting.")
