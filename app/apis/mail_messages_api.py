from app.apis.endpoint import EndPoint
import requests, logging
from app.utils.string import request_timeout_msg, request_http_error_msg
from app.models.user import User


class MailMessagesAPI(EndPoint):
    def __init__(
        self,
        role: str = "admin",
        user: User = None,
        client=None,
    ):
        super().__init__(role, user, client)
        self.url = self.uri + "mail-messages/"

    def get_mail_messages_by_query(self, skip: int, take: int) -> dict:
        payload = {"skip": skip, "take": take, "requireTotalCount": True}
        if self.client is None:
            r = requests.get(self.url + "query", headers=self.headers, params=payload)
            r.raise_for_status()
            return r.json()
        with self.client.get(
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
