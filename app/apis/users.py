from curses.ascii import US
from endpoint import EndPoint
import requests


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
            print("Response could not be decoded as JSON")


def main():
    users_api = Users()
    print(users_api.get_users())


if __name__ == "__main__":
    main()
