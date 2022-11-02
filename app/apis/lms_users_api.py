import requests, logging
from app.apis.endpoint import EndPoint
from app.models.user import User
from app.drivers.database_driver import DatabaseDriver
from app.utils.string import request_timeout_msg, request_http_error_msg


class LmsUsersAPI(EndPoint):
    def __init__(self, driver: DatabaseDriver):
        super().__init__()
        self.url = self.uri + "lms-users/"
        self.driver = driver

    def get_users(self, client=None) -> list[dict]:
        if client is None:
            r = requests.get(self.url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with client.get(
            self.url,
            headers=self.headers,
            name="get users",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_user(self, client=None) -> User:
        new_user = User.gen_random_object()
        if client is None:
            r = requests.post(
                self.url, json=new_user.to_dict_for_creating(), headers=self.headers
            )
            r.raise_for_status()
            new_user.id = r.json()["id"]
        else:
            with client.post(
                self.url,
                json=new_user.to_dict_for_creating(),
                headers=self.headers,
                name="create user",
                catch_response=True,
            ) as response:
                if response.ok:
                    new_user.id = response.json()["id"]
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        self.driver.insert_one_user(new_user.to_dict_for_database())
        return new_user

    def update_user(self, user: User, client=None):
        user = user.gen_random_update()
        if client is None:
            r = requests.put(
                self.url + user.id,
                json=user.to_dict_for_updating(),
                headers=self.headers,
            )
            r.raise_for_status()
        else:
            with client.put(
                self.url + user.id,
                json=user.to_dict_for_updating(),
                headers=self.headers,
                name="update user",
                catch_response=True,
            ) as response:
                if not response.ok:
                    response.failure(request_http_error_msg(response))
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
        self.driver.update_user(user.to_dict_for_database())

    def get_user_by_id(self, id: str, client=None) -> dict:
        if client is None:
            r = requests.get(self.url + id, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with client.get(
            self.url + id,
            headers=self.headers,
            name="get user by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def delete_user(self, id: str, client=None) -> dict:
        # not work
        r = requests.delete(self.url + id, headers=self.headers)
        r.raise_for_status()
        return r.json()


def main():
    import random

    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        filename="users_api.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    lms_users_api = LmsUsersAPI()
    users = lms_users_api.get_users()
    print(users)
    # user_to_update = random.choice(User.filter_original_users(users))
    print(lms_users_api.create_user())
    # user_to_update = lms_users_api.get_one_user("8e5cb704-2283-487a-86dd-f9957e91d99d")
    # print(lms_users_api.update_one_user(user_to_update))
    user_to_delete = random.choice(User.filter_original_users(users))
    print(lms_users_api.delete_user(user_to_delete["id"]))


if __name__ == "__main__":
    main()
