from app.apis.endpoint import EndPoint
import requests, logging


class MailMessagesAPI(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "mail-messages/"

    def get_mail_messages_by_query(self, skip: int, take: int) -> dict:
        payload = {"skip": skip, "take": take, "requireTotalCount": True}
        r = requests.get(self.url + "query", headers=self.headers, params=payload)
        r.raise_for_status()
        res = r.json()
        return res
