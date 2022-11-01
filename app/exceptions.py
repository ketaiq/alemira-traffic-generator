class NoResetPasswordUrlException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnsupportedModeException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
