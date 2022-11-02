import requests, json
from functools import lru_cache
from app.models.user import User


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

    def __init__(self, user: User = None):
        self.uri = self.URI
        self.headers = self.get_headers(user.to_dict_for_login())

    @lru_cache(maxsize=None)
    def _get_token(self, user=None):
        """
        :param user:
        :return:
        """
        if isinstance(user, str):
            user = json.loads(user)
        response = requests.post(
            self.IDENTITY_SERVER + "connect/token",
            data=user,
        )
        json_response = response.json()
        return json_response.get("access_token")

    def get_headers(
        self,
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

        token = self._get_token(user)
        return {
            "accept": "*/*",
            "Authorization": "Bearer " + token,
        }


def main():
    end_point = EndPoint()
    print(end_point.get_headers())


if __name__ == "__main__":
    main()
