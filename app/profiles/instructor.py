from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI


class Instructor:
    """A class to represent the profile of instructors."""

    def __init__(
        self,
        lms_users_api: LmsUsersAPI,
        mail_messages_api: MailMessagesAPI,
        account_reset_password_api: AccountResetPasswordAPI,
        client=None,
    ):
        self.lms_users_api = lms_users_api
        self.mail_messages_api = mail_messages_api
        self.account_reset_password_api = account_reset_password_api
        self.client = client

    def enroll_one_student(self):
        pass

    def enroll_group(self):
        pass

    def update_objective(self):
        pass
