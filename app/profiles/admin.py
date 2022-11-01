import logging
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI


class Admin:
    """A class to represent the profile of administrators."""

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

    def create_user(self):
        """Create a user with a random profile."""
        new_user = self.lms_users_api.create_user(self.client)
        skip = 0
        mail_messages = self.mail_messages_api.get_mail_messages_by_query(skip, 10)

        try:
            mail = next(
                mail for mail in mail_messages if mail.is_sent_to_user(new_user)
            )
            url = mail.get_reset_password_url()
            self.account_reset_password_api.reset_password(url, new_user)
        except StopIteration:
            logging.error(f"No mail is sent to user {new_user.username}.")
