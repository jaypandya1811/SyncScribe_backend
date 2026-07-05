class MeetingResultNotFound(Exception):

    def __init__(self):

        super().__init__("No meeting results found.")

class MeetingResultUpdateError(Exception):

    def __init__(self):

        super().__init__("Unable to update meeting result.")
