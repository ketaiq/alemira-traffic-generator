class RequiredObjectNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResetPasswordUrlNotFoundException(RequiredObjectNotFoundException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class MailNotFoundException(RequiredObjectNotFoundException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserNotFoundException(RequiredObjectNotFoundException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ObjectiveNotFoundException(RequiredObjectNotFoundException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ActivityNotFoundException(RequiredObjectNotFoundException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class RoleNotFoundException(RequiredObjectNotFoundException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ObjectivePersonalEnrollmentNotFoundException(RequiredObjectNotFoundException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
