from app.apis.endpoint import EndPoint
from app.models.user import User
from app.utils.string import request_timeout_msg, request_http_error_msg
import requests, logging


class RolesAPI(EndPoint):
    def __init__(
        self,
        role: str = "admin",
        user: User = None,
        client=None,
    ):
        super().__init__(role, user, client)
        self.url = self.uri + "roles/"

    def get_roles_by_query(self, query: dict) -> dict:
        if self.client is None:
            r = requests.get(self.url + "query", headers=self.headers, params=query)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "query",
            headers=self.headers,
            params=query,
            name="get roles by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))
