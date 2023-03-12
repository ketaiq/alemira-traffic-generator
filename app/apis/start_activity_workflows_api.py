from app.apis.user_api_endpoint import UserAPIEndPoint
import requests
from app.utils.string import request_http_error_msg, request_timeout_msg
from app.utils.time import sleep_for_seconds
import logging


class StartActivityWorkflowsAPI(UserAPIEndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client=client)
        self.url = self.uri + "start-activity-workflows/"

    def get_started_activity_workflow_state_by_id(self, headers: dict, id: str) -> dict:
        if self.client is None:
            r = requests.get(self.url + id, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + id,
            headers=headers,
            name="get started activity workflow state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_started_activity_workflows(self, headers: dict) -> list:
        if self.client is None:
            r = requests.get(self.url, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url,
            headers=headers,
            name="get started activity workflows",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def start_activity_workflow(self, headers: dict, objective_workflow_id: str):
        headers["Prefer"] = "respond-async"
        payload = {
            "activityPartIds": [],
            "objectiveWorkflowId": objective_workflow_id,
        }
        if self.client is None:
            r = requests.post(self.url, json=payload, headers=headers)
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            for _ in range(10):
                created_state = self.get_started_activity_workflow_state_by_id(
                    headers, created_id
                )
                if created_state["completed"]:
                    break
                sleep_for_seconds(3, 5)
        else:
            with self.client.post(
                self.url,
                json=payload,
                headers=headers,
                name="start activity workflow",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = response.json()["id"]
                    # check entity is created successfully
                    for _ in range(10):
                        created_state = self.get_started_activity_workflow_state_by_id(
                            headers, created_id
                        )
                        if created_state["completed"]:
                            break
                        sleep_for_seconds(3, 5)
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
