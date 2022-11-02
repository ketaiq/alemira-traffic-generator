from app.apis.endpoint import EndPoint
import requests, logging
from app.utils.string import request_timeout_msg, request_http_error_msg


class MailMessagesAPI(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "mail-messages/"

    def get_mail_messages_by_query(self, skip: int, take: int, client=None) -> dict:
        payload = {"skip": skip, "take": take, "requireTotalCount": True}
        if client is None:
            r = requests.get(self.url + "query", headers=self.headers, params=payload)
            r.raise_for_status()
            return r.json()
        with client.get(
            self.url + "query",
            headers=self.headers,
            params=payload,
            name="get mail messages by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))
