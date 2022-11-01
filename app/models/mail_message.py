import logging
from app.models.model import Model
import re
from app.models.user import User
from app.exceptions import ResetPasswordUrlNotFoundException


class MailMessage(Model):
    FIELD_NAMES = (
        "id",
        "toName",
        "toAddress",
        "subject",
        "textBody",
        "htmlBody",
        "created",
        "modified",
        "state",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.FIELD_NAMES,
            *args,
            **kwargs,
        )

    def get_reset_password_url(self) -> str:
        try:
            if self.htmlBody:
                match = re.search(r"href='(.*)'>", self.htmlBody)
                if match:
                    return match.group(1)
                raise ResetPasswordUrlNotFoundException(
                    "No URL is matched in htmlBody."
                )
            raise ResetPasswordUrlNotFoundException(
                f"Invalid htmlBody: {self.htmlBody}."
            )
        except ResetPasswordUrlNotFoundException as e:
            logging.error(e.message)

    def is_sent_to_user(self, user: User) -> bool:
        return self.toAddress == user.email
