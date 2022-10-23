import requests, logging
from app.apis.endpoint import EndPoint
from app.models.user import User


class Users(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "lms-users"

    def get_users(self) -> list[dict]:
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        try:
            users = r.json()
            return users
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def create_user(self):
        new_user = User.gen_random_object()
        r = requests.post(self.url, json=new_user.to_dict(), headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        filename="users_api.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    users_api = Users()
    print(users_api.get_users())
    print(users_api.create_user())


if __name__ == "__main__":
    main()
