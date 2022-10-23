import requests, logging
from app.apis.endpoint import EndPoint
from app.models.user import User


class LmsUsers(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "lms-users/"

    def get_users(self) -> list[dict]:
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        try:
            users = r.json()
            return users
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def create_one_user(self) -> dict:
        new_user = User.gen_random_object()
        r = requests.post(self.url, json=new_user.to_dict(), headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def update_one_user(self, user_dict: dict):
        user = User(user_dict)
        user.gen_random_update()
        r = requests.put(self.url + user.id, json=user.to_dict(), headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def get_one_user(self, id: str) -> dict:
        r = requests.get(self.url + id, headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def delete_one_user(self, id: str) -> dict:
        # not work
        r = requests.delete(self.url + id, headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")


def main():
    import random

    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        filename="users_api.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    lms_users_api = LmsUsers()
    users = lms_users_api.get_users()
    print(users)
    # user_to_update = random.choice(User.filter_original_users(users))
    # print(lms_users_api.create_user())
    # user_to_update = lms_users_api.get_one_user("8e5cb704-2283-487a-86dd-f9957e91d99d")
    # print(lms_users_api.update_one_user(user_to_update))
    user_to_delete = random.choice(User.filter_original_users(users))
    # print(lms_users_api.delete_one_user(user_to_delete["id"])) 


if __name__ == "__main__":
    main()