import logging
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI
from app.exceptions import MailNotFoundException
from app.models.mail_message import MailMessage


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
        take = 10
        try:
            while True:
                res = self.mail_messages_api.get_mail_messages_by_query(skip, take)
                remaining_count = res["totalCount"] - take - skip
                mail_messages = [MailMessage(msg) for msg in res["data"]]
                mail = next(
                    (mail for mail in mail_messages if mail.is_sent_to_user(new_user)),
                    None,
                )
                skip += take
                if mail is not None:
                    url = mail.get_reset_password_url()
                    self.account_reset_password_api.reset_password(url, new_user)
                    break
                if remaining_count <= 0:
                    raise MailNotFoundException(
                        f"No mail is sent to user {new_user.username}."
                    )
        except MailNotFoundException as e:
            logging.error(e.message)
