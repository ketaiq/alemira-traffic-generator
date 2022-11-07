from app.apis.user_api_endpoint import UserAPIEndPoint
import requests, uuid
from app.utils.string import request_http_error_msg, request_timeout_msg


class StartObjectiveWorkflowsAPI(UserAPIEndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client=client)
        self.url = self.uri + "start-objective-workflows/"

    def get_started_objective_workflow_state_by_id(
        self, headers: dict, id: str
    ) -> dict:
        if self.client is None:
            r = requests.get(self.url + id, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + id,
            headers=headers,
            name="get started objective workflow state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def start_objective_workflow(
        self, headers: dict, objective_workflow_aggregate_id: str
    ) -> str:
        objective_workflow_id = None
        payload = {
            "id": str(uuid.uuid4()),
            "objectiveWorkflowAggregateId": objective_workflow_aggregate_id,
        }
        if self.client is None:
            r = requests.post(self.url, json=payload, headers=headers)
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            while True:
                created_state = self.get_started_objective_workflow_state_by_id(
                    headers, created_id
                )
                if created_state["completed"]:
                    objective_workflow_id = created_state["entityId"]
                    break
        else:
            with self.client.post(
                self.url,
                json=payload,
                headers=headers,
                name="start objective workflow",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = response.json()["id"]
                    # check entity is created successfully
                    while True:
                        created_state = self.get_started_objective_workflow_state_by_id(
                            headers, created_id
                        )
                        if created_state["completed"]:
                            objective_workflow_id = created_state["entityId"]
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        return objective_workflow_id
