import requests, json, logging
from functools import lru_cache
from app.models.user import User
from app.utils.string import request_http_error_msg, request_timeout_msg


class EndPoint:
    IDENTITY_SERVER = "https://identity.alms.dev.alemira.com/"
    DEFAULT_USER = {
        "username": "alice@company.com",
        "password": "Pass123$",
        "client_id": "insomnia",
        "client_secret": "insomnia",
        "grant_type": "password",
    }
    URI = "https://userapi.alms.dev.alemira.com/api/v1/"
    FILE_URI = "https://alms.dev.alemira.com/fileapi/api/v1/"
    TIMEOUT_MAX = 180

    def __init__(self, role: str, user: User, client):
        self.uri = self.URI
        self.file_uri = self.FILE_URI
        self.client = client
        if user is None:
            self.headers = self.get_headers(role)
        else:
            self.headers = self.get_headers(role, user.to_dict_for_login())

    @lru_cache(maxsize=None)
    def _get_token(self, role: str, user=None):
        """
        :param user:
        :return:
        """
        if isinstance(user, str):
            user = json.loads(user)
        if self.client is None:
            r = requests.post(
                self.IDENTITY_SERVER + "connect/token",
                data=user,
            )
            r.raise_for_status()
            return r.json().get("access_token")
        with self.client.post(
            self.IDENTITY_SERVER + "connect/token",
            data=user,
            name=f"login {role} user",
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
        role: str,
        user: dict = None,
    ):
        """
        :param with_auth:
        :param user:
        :return:
        """
        if user is None:
            user = json.dumps(self.DEFAULT_USER)
        if isinstance(user, dict):
            # for lru_cache user always should be hashable
            # overriding user credentials with insomnia
            user = json.dumps({**self.DEFAULT_USER, **user})

        token = self._get_token(role, user)
        return {
            "accept": "*/*",
            "Authorization": "Bearer " + token,
        }


def main():
    end_point = EndPoint()
    print(end_point.get_headers())


if __name__ == "__main__":
    main()
