from app.apis.user_api_endpoint import UserAPIEndPoint
from app.models.user import User
from app.utils.string import request_timeout_msg, request_http_error_msg
import requests, logging


class UserRolesAPI(UserAPIEndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "user-roles/"

    def get_created_user_role_state_by_id(self, headers: dict, id: str) -> dict:
        url = self.uri + "create-user-roles/" + id
        if self.client is None:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            url,
            headers=headers,
            name="get created user role state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_user_role(self, headers: dict, user_id: str, role_id: str):
        payload = {"userId": user_id, "roleId": role_id}
        if self.client is None:
            r = requests.post(
                self.url,
                json=payload,
                headers=headers,
            )
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            while True:
                created_state = self.get_created_user_role_state_by_id(
                    headers, created_id
                )
                if created_state["completed"]:
                    break
        else:
            with self.client.post(
                self.url,
                json=payload,
                headers=headers,
                name="create user role",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = response.json()["id"]
                    # check entity is created successfully
                    while True:
                        created_state = self.get_created_user_role_state_by_id(
                            headers, created_id
                        )
                        if created_state["completed"]:
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
