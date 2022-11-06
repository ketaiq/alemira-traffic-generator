from app.apis.endpoint import EndPoint
import requests
from app.utils.string import request_http_error_msg, request_timeout_msg


class StartActivityWorkflowsAPI(EndPoint):
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

    def start_activity_workflow(self, headers: dict, objective_workflow_id: str):
        payload = {
            "activityPartIds": [],
            "objectiveWorkflowId": objective_workflow_id,
        }
        if self.client is None:
            r = requests.post(self.url, json=payload, headers=headers)
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            while True:
                created_state = self.get_started_activity_workflow_state_by_id(
                    headers, created_id
                )
                if created_state["completed"]:
                    break
        else:
            with self.client.post(
                self.url,
                json=payload,
                headers=headers,
                name="start activity workflow",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = r.json()["id"]
                    # check entity is created successfully
                    while True:
                        created_state = self.get_started_activity_workflow_state_by_id(
                            headers, created_id
                        )
                        if created_state["completed"]:
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
