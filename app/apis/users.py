from curses.ascii import US
from endpoint import EndPoint
import requests, logging


class Users(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "users"

    def get_users(self) -> list[dict]:
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        try:
            users = r.json()
            return users
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def create_user(self):

        r = requests.post(
            self.url,
        )


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    users_api = Users()
    print(users_api.get_users())


if __name__ == "__main__":
    main()
