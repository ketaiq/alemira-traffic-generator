class ResetPasswordUrlNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class MailNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ObjectiveNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnsupportedModeException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
