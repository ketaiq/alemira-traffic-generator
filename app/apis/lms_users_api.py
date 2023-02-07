import requests, logging
from app.apis.user_api_endpoint import UserAPIEndPoint
from app.models.user import User
from app.drivers.database_driver import DatabaseDriver
from app.utils.string import request_timeout_msg, request_http_error_msg
from app.models.role import Role
from app.utils.time import sleep_for_seconds


class LmsUsersAPI(UserAPIEndPoint):
    def __init__(
        self,
        driver: DatabaseDriver,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "lms-users/"
        self.driver = driver

    def get_user_me(self, headers: dict) -> User:
        if self.client is None:
            r = requests.get(self.url + "me", headers=headers)
            r.raise_for_status()
            return User(r.json())
        with self.client.get(
            self.url + "me",
            headers=headers,
            name="get user me",
            catch_response=True,
        ) as response:
            if response.ok:
                return User(response.json())
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_users(self, headers: dict) -> list[dict]:
        if self.client is None:
            r = requests.get(self.url, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url,
            headers=headers,
            name="get users",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_created_user_state_by_id(self, headers: dict, id: str) -> dict:
        if self.client is None:
            r = requests.get(self.uri + "create-lms-users/" + id, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "create-lms-users/" + id,
            headers=headers,
            name="get created user state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_updated_user_state_by_id(self, headers: dict, id: str) -> dict:
        if self.client is None:
            r = requests.get(self.uri + "update-lms-users/" + id, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "update-lms-users/" + id,
            headers=headers,
            name="get updated user state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_user(self, headers: dict, role: Role) -> User:
        while True:
            new_user = User.gen_random_object()
            user_emails = self.get_users_by_query(
                headers,
                {
                    "skip": 0,
                    "take": 10,
                    "requireTotalCount": True,
                    "filter": f'["email","contains","{new_user.email}"]',
                },
            )
            # check user email does not exist
            if len(user_emails["data"]) == 0:
                break

        if self.client is None:
            r = requests.post(
                self.url, json=new_user.to_dict_for_creating(), headers=headers
            )
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            for _ in range(10):
                created_state = self.get_created_user_state_by_id(headers, created_id)
                if created_state["completed"]:
                    new_user.id = created_state["entityId"]
                    break
                sleep_for_seconds(1, 3)
        else:
            with self.client.post(
                self.url,
                json=new_user.to_dict_for_creating(),
                headers=headers,
                name=f"create {role.value} user",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = response.json()["id"]
                    # check entity is created successfully
                    for _ in range(10):
                        created_state = self.get_created_user_state_by_id(
                            headers, created_id
                        )
                        if created_state["completed"]:
                            new_user.id = created_state["entityId"]
                            break
                        sleep_for_seconds(1, 3)
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        new_user._role = role.value
        self.driver.insert_one_user(new_user)
        return new_user

    def update_user(self, headers: dict, user: User):
        if self.client is None:
            r = requests.put(
                self.url + user.id,
                json=user.to_dict_for_updating(),
                headers=headers,
            )
            r.raise_for_status()
            updated_id = r.json()["id"]
            # check entity is updated successfully
            for _ in range(10):
                updated_state = self.get_updated_user_state_by_id(headers, updated_id)
                if updated_state["completed"]:
                    break
                sleep_for_seconds(1, 3)
        else:
            with self.client.put(
                self.url + user.id,
                json=user.to_dict_for_updating(),
                headers=headers,
                name="update user",
                catch_response=True,
            ) as response:
                if response.ok:
                    updated_id = response.json()["id"]
                    # check entity is updated successfully
                    for _ in range(10):
                        updated_state = self.get_updated_user_state_by_id(
                            headers, updated_id
                        )
                        if updated_state["completed"]:
                            break
                        sleep_for_seconds(1, 3)
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        self.driver.update_user(user)

    def get_user_by_id(self, headers: dict, id: str) -> User:
        if self.client is None:
            r = requests.get(self.url + id, headers=headers)
            r.raise_for_status()
            return User(r.json())
        with self.client.get(
            self.url + id,
            headers=headers,
            name="get user by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return User(response.json())
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_users_by_query(self, headers: dict, query: str) -> dict:
        if self.client is None:
            r = requests.get(self.url + "query", headers=headers, params=query)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "query",
            headers=headers,
            params=query,
            name="get users by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def delete_user(self, headers: dict, id: str) -> dict:
        # not work
        r = requests.delete(self.url + id, headers=headers)
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
