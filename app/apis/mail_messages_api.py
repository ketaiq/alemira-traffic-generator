from app.apis.endpoint import EndPoint
import requests, logging
from app.models.mail_message import MailMessage


class MailMessagesAPI(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "mail-messages/"

    def get_mail_messages_by_query(self, skip: int, take: int) -> list[MailMessage]:
        payload = {"skip": skip, "take": take}
        r = requests.get(self.url + "query", headers=self.headers, params=payload)
        r.raise_for_status()
        messages = r.json()["data"]
        return [MailMessage(msg) for msg in messages]
