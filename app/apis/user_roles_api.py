from app.apis.endpoint import EndPoint
from app.models.user import User
from app.utils.string import request_timeout_msg, request_http_error_msg
import requests, logging


class UserRolesAPI(EndPoint):
    def __init__(
        self,
        role: str = "admin",
        user: User = None,
        client=None,
    ):
        super().__init__(role, user, client)
        self.url = self.uri + "user-roles/"

    def get_created_user_role_state_by_id(self, id: str) -> dict:
        url = self.uri + "create-user-roles/" + id
        if self.client is None:
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            url,
            headers=self.headers,
            name="get created user role state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_user_role(self, user_id: str, role_id: str):
        payload = {"userId": user_id, "roleId": role_id}
        if self.client is None:
            r = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
            )
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            while True:
                created_state = self.get_created_user_role_state_by_id(created_id)
                if created_state["completed"]:
                    break
        else:
            with self.client.post(
                self.url,
                json=payload,
                headers=self.headers,
                name="create user role",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = r.json()["id"]
                    # check entity is created successfully
                    while True:
                        created_state = self.get_created_user_role_state_by_id(
                            created_id
                        )
                        if created_state["completed"]:
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
