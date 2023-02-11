class UnsupportedAnythingException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnsupportedModeException(UnsupportedAnythingException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnsupportedUserException(UnsupportedAnythingException):
    def __init__(self, user):
        self.message = f"User {user} doesn't exist!"
        super().__init__(self.message)


class UnsupportedDayException(UnsupportedAnythingException):
    def __init__(self, day):
        self.message = f"Day {day} doesn't exist!"
        super().__init__(self.message)
