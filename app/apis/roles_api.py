from app.apis.user_api_endpoint import UserAPIEndPoint
from app.models.user import User
from app.utils.string import request_timeout_msg, request_http_error_msg
import requests, logging


class RolesAPI(UserAPIEndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "roles/"

    def get_roles_by_query(self, headers: dict, query: dict) -> dict:
        if self.client is None:
            r = requests.get(self.url + "query", headers=headers, params=query)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "query",
            headers=headers,
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
