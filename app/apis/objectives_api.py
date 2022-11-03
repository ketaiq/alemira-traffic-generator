from app.apis.endpoint import EndPoint
from app.drivers.database_driver import DatabaseDriver
import requests
from app.utils.string import request_timeout_msg, request_http_error_msg
from app.models.objective.objective import Objective
from app.models.activity.activity import Activity


class ObjectivesAPI(EndPoint):
    def __init__(self, driver: DatabaseDriver):
        super().__init__()
        self.url = self.uri + "objectives/"
        self.driver = driver

    def get_objective_by_id(self, id: str, client=None) -> Objective:
        if client is None:
            r = requests.get(self.url + id, headers=self.headers)
            r.raise_for_status()
            return r.json()
        with client.get(
            self.url + id,
            headers=self.headers,
            name="get objective by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return Objective(response.json())
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_objective(self, activity: Activity):
        objective = Objective.gen_object_from_activity(activity)
        r = requests.post(
            self.url, json=objective.to_dict_for_creating(), headers=self.headers
        )
        r.raise_for_status()
        objective.id = r.json()["id"]
        self.driver.insert_one_objective(objective)

    def update_objective(self, objective: Objective, client=None):
        objective = objective.gen_random_update()
        if client is None:
            r = requests.put(
                self.url + objective.id,
                json=objective.to_dict_for_updating(),
                headers=self.headers,
            )
            r.raise_for_status()
        else:
            with client.put(
                self.url + objective.id,
                json=objective.to_dict_for_updating(),
                headers=self.headers,
                name="update objective",
                catch_response=True,
            ) as response:
                if not response.ok:
                    response.failure(request_http_error_msg(response))
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
        self.driver.update_objective(objective)
