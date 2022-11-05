import requests, logging
from app.apis.endpoint import EndPoint
from app.models.user import User
from app.drivers.database_driver import DatabaseDriver
from app.utils.string import request_timeout_msg, request_http_error_msg


class LmsUsersAPI(EndPoint):
    def __init__(
        self,
        driver: DatabaseDriver,
        role: str = "admin",
        user: User = None,
        client=None,
    ):
        super().__init__(role, user, client)
        self.url = self.uri + "lms-users/"
        self.driver = driver

    def get_users(self) -> list[dict]:
        if self.client is None:
            r = requests.get(self.url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
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

    def get_created_user_state_by_id(self, id: str) -> dict:
        if self.client is None:
            r = requests.get(self.uri + "create-lms-users/" + id, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "create-lms-users/" + id,
            headers=self.headers,
            name="get created user state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_updated_user_state_by_id(self, id: str) -> dict:
        if self.client is None:
            r = requests.get(self.uri + "update-lms-users/" + id, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "update-lms-users/" + id,
            headers=self.headers,
            name="get updated user state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_user(self) -> User:
        new_user = User.gen_random_object()
        if self.client is None:
            r = requests.post(
                self.url, json=new_user.to_dict_for_creating(), headers=self.headers
            )
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            while True:
                created_state = self.get_created_user_state_by_id(created_id)
                if created_state["completed"]:
                    new_user.id = created_state["entityId"]
                    break
        else:
            with self.client.post(
                self.url,
                json=new_user.to_dict_for_creating(),
                headers=self.headers,
                name="create user",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = r.json()["id"]
                    # check entity is created successfully
                    while True:
                        created_state = self.get_created_user_state_by_id(
                            created_id, self.client
                        )
                        if created_state["completed"]:
                            new_user.id = created_state["entityId"]
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        self.driver.insert_one_user(new_user)
        return new_user

    def update_user(self, user: User):
        if self.client is None:
            r = requests.put(
                self.url + user.id,
                json=user.to_dict_for_updating(),
                headers=self.headers,
            )
            r.raise_for_status()
            updated_id = r.json()["id"]
            # check entity is created successfully
            while True:
                updated_state = self.get_created_user_state_by_id(updated_id)
                if updated_state["completed"]:
                    break
        else:
            with self.client.put(
                self.url + user.id,
                json=user.to_dict_for_updating(),
                headers=self.headers,
                name="update user",
                catch_response=True,
            ) as response:
                if response.ok:
                    updated_id = r.json()["id"]
                    # check entity is created successfully
                    while True:
                        updated_state = self.get_created_user_state_by_id(
                            updated_id, self.client
                        )
                        if updated_state["completed"]:
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        self.driver.update_user(user)

    def get_user_by_id(self, id: str) -> User:
        if self.client is None:
            r = requests.get(self.url + id, headers=self.headers)
            r.raise_for_status()
            return User(r.json())
        with self.client.get(
            self.url + id,
            headers=self.headers,
            name="get user by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return User(response.json())
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def delete_user(self, id: str) -> dict:
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
