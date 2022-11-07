from app.apis.user_api_endpoint import UserAPIEndPoint
import requests, logging
from app.utils.string import request_http_error_msg, request_timeout_msg


class FinishActivityWorkflow(UserAPIEndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "finish-activity-workflows/"

    def get_created_finish_activity_workflow_state_by_id(
        self, headers: dict, id: str
    ) -> dict:
        if self.client is None:
            r = requests.get(self.url + id, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + id,
            headers=headers,
            name="get created finish activity workflow state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_finish_activity_workflow(
        self, headers: dict, activity_workflow_ids: list, objective_workflow_id: str
    ):
        payload = {
            "activityWorkflowIds": activity_workflow_ids,
            "objectiveWorkflowId": objective_workflow_id,
        }
        if self.client is None:
            r = requests.post(self.url, json=payload, headers=headers)
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            while True:
                created_state = self.get_created_finish_activity_workflow_state_by_id(
                    headers, created_id
                )
                if created_state["completed"]:
                    break
        else:
            with self.client.post(
                self.url,
                json=payload,
                headers=headers,
                name=f"create finish activity workflow",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = response.json()["id"]
                    # check entity is created successfully
                    while True:
                        created_state = (
                            self.get_created_finish_activity_workflow_state_by_id(
                                headers, created_id
                            )
                        )
                        if created_state["completed"]:
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
