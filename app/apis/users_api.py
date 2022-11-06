import requests, logging
from app.apis.user_api_endpoint import UserAPIEndPoint
from app.utils.string import request_timeout_msg, request_http_error_msg
from app.models.user import User


class UsersAPI(UserAPIEndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "users/"

    def get_user_objective_workflow_aggregates(
        self, headers: dict, user_id: str
    ) -> list:
        if self.client is None:
            r = requests.get(
                self.url + user_id + "/objective-workflow-aggregates/",
                headers=headers,
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + user_id + "/objective-workflow-aggregates/",
            headers=headers,
            name="get user objective workflow aggregates",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_user_activity_workflow_aggregates_by_query(
        self, headers: dict, query: dict
    ) -> dict:
        if self.client is None:
            r = requests.get(
                self.url + "me/activity-workflow-aggregates/query",
                headers=headers,
                params=query,
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "me/activity-workflow-aggregates/query",
            headers=headers,
            params=query,
            name="get user activity workflow aggregates by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_users_by_query(self, headers: dict, query: dict) -> dict:
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
