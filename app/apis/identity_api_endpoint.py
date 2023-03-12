from functools import lru_cache
import requests, json, logging
from app.models.user import User
from app.models.role import Role
from app.utils.string import request_http_error_msg, request_timeout_msg
from app.utils.time import sleep_for_seconds


class IdentityAPIEndPoint:
    URI = "https://identity.alms.crab.alemira.com/"
    DEFAULT_USER = {
        "username": "alice@company.com",
        "password": "Pass123$",
        "client_id": "insomnia",
        "client_secret": "insomnia",
        "grant_type": "password",
    }
    TIMEOUT_MAX = 180

    def __init__(self, client=None):
        self.uri = self.URI
        self.client = client

    def _get_token(self, role: str, user: str) -> str:
        user = json.loads(user)
        if self.client is None:
            r = requests.post(
                IdentityAPIEndPoint.URI + "connect/token",
                data=user,
            )
            r.raise_for_status()
            return r.json().get("access_token")
        with self.client.post(
            IdentityAPIEndPoint.URI + "connect/token",
            data=user,
            name=f"login {role} user".lower(),
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json().get("access_token")
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_headers(
        self,
        role: Role,
        user: User = None,
    ) -> dict:
        if user is None:
            user = json.dumps(self.DEFAULT_USER)
        else:
            user = user.to_dict_for_login()
            # for lru_cache user always should be hashable
            # overriding user credentials with insomnia
            user = json.dumps({**self.DEFAULT_USER, **user})
        # try 10 times if token is none or empty
        for _ in range(10):
            token = self._get_token(role.value, user)
            if token:
                break
            sleep_for_seconds(3, 5)
        username = json.loads(user)["username"]
        logging.info(f"{role.value} {username} login")
        return {
            "accept": "*/*",
            "Authorization": "Bearer " + token,
        }
