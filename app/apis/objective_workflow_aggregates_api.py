from app.apis.endpoint import EndPoint
from app.models.user import User
import requests
from app.utils.string import request_http_error_msg, request_timeout_msg


class ObjectiveWorkflowAggregatesAPI(EndPoint):
    def __init__(
        self,
        role: str = "admin",
        user: User = None,
        client=None,
    ):
        super().__init__(role, user, client)
        self.url = self.uri + "objective-workflow-aggregates/"

    def get_objective_workflow_aggregate_by_id(self, id: str) -> dict:
        if self.client is None:
            r = requests.get(self.url + id, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + id,
            headers=self.headers,
            name="get objective workflow aggregate by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_objective_records_by_id(self, id: str) -> list:
        url = self.url + id + "/objective-records"
        if self.client is None:
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            url,
            headers=self.headers,
            name="get objective records by objective workflow aggregate id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_activity_with_aggregates_by_id(
        self, headers: dict, objective_workflow_aggregate_id: str, activity_id: str
    ) -> dict:
        url = (
            self.url
            + objective_workflow_aggregate_id
            + "/activity-with-aggregates/"
            + activity_id
        )
        if self.client is None:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            url,
            headers=headers,
            name="get activity with aggregates by objective workflow aggregate id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))
