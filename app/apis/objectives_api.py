from app.apis.endpoint import EndPoint
from app.drivers.database_driver import DatabaseDriver
import requests
from app.utils.string import request_timeout_msg, request_http_error_msg
from app.models.objective.objective import Objective
from app.models.activity.activity import Activity
from app.models.user import User


class ObjectivesAPI(EndPoint):
    def __init__(
        self,
        driver: DatabaseDriver,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "objectives/"
        self.file_url = self.file_uri + "objectives/"
        self.driver = driver

    def get_objective_by_id(self, headers: dict, id: str) -> Objective:
        if self.client is None:
            r = requests.get(self.url + id, headers=headers)
            r.raise_for_status()
            return Objective(r.json())
        with self.client.get(
            self.url + id,
            headers=headers,
            name="get objective by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return Objective(response.json())
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_objectives_by_query(self, headers: dict, query: dict) -> dict:
        if self.client is None:
            r = requests.get(self.url + "query", headers=headers, params=query)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "query",
            headers=headers,
            params=query,
            name="get objectives by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_objective_by_code_or_none(
        self, headers: dict, code: str
    ) -> Objective | None:
        skip = 0
        take = 10
        while True:
            res = self.get_objectives_by_query(
                headers, {"skip": skip, "take": take, "requireTotalCount": True}
            )
            remaining_count = res["totalCount"] - take - skip
            objective = next(
                (objective for objective in res["data"] if objective["code"] == code),
                None,
            )
            skip += take
            if objective is not None:
                return Objective(objective)
            if remaining_count <= 0:
                break
        return None

    def get_created_objective_state_by_id(self, headers: dict, id: str) -> str:
        r = requests.get(self.uri + "create-objectives/" + id, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_updated_objective_state_by_id(self, headers: dict, id: str) -> str:
        if self.client is None:
            r = requests.get(self.uri + "update-objectives/" + id, headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "update-objectives/" + id,
            headers=headers,
            name="get updated objective state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_objective_personal_enrollments_by_query(
        self, headers: dict, objective_id: str, query: dict
    ) -> dict:
        if self.client is None:
            r = requests.get(
                self.url + objective_id + "/personal-enrollments/query",
                headers=headers,
                params=query,
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + objective_id + "/personal-enrollments/query",
            headers=headers,
            params=query,
            name="get objective personal enrollments by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_objective_workflow_aggregate_by_id(
        self, headers: dict, objective_id: str
    ) -> dict:
        if self.client is None:
            r = requests.get(
                self.url + objective_id + "/objective-workflow-aggregate",
                headers=headers,
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + objective_id + "/objective-workflow-aggregate",
            headers=headers,
            name="get objective workflow aggregate by objective id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def create_objective(self, headers: dict, activity: Activity) -> str:
        """Create objective and return a created id."""
        objective = Objective.gen_object_from_activity(activity)
        r = requests.post(
            self.url, json=objective.to_dict_for_creating(), headers=headers
        )
        r.raise_for_status()
        objective.id = self.get_created_objective_state_by_id(headers, r.json()["id"])
        self.driver.insert_one_objective(objective)
        return r.json()["id"]

    def update_objective(self, headers: dict, objective: Objective):
        if self.client is None:
            r = requests.put(
                self.url + objective.id,
                json=objective.to_dict_for_updating(),
                headers=headers,
            )
            r.raise_for_status()
            updated_id = r.json()["id"]
            # check entity is updated successfully
            while True:
                updated_state = self.get_updated_objective_state_by_id(
                    headers, updated_id
                )
                if updated_state["completed"]:
                    break
        else:
            with self.client.put(
                self.url + objective.id,
                json=objective.to_dict_for_updating(),
                headers=headers,
                name="update objective",
                catch_response=True,
            ) as response:
                if response.ok:
                    updated_id = r.json()["id"]
                    # check entity is updated successfully
                    while True:
                        updated_state = self.get_updated_objective_state_by_id(
                            headers, updated_id
                        )
                        if updated_state["completed"]:
                            break
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        self.driver.update_objective(objective)

    def upload_image_to_objective(
        self, headers: dict, objective: Objective, image_filename: str
    ):
        files = {"file": open(f"resources/images/{image_filename}", "rb")}
        image_url = ""
        if self.client is None:
            r = requests.post(
                self.file_url + objective.id + "/public-files",
                files=files,
                headers=headers,
            )
            r.raise_for_status()
            image_url = r.json()["url"]
        else:
            with self.client.post(
                self.file_url + objective.id + "/public-files",
                files=files,
                headers=headers,
                name="upload image to objective",
                catch_response=True,
            ) as response:
                if response.ok:
                    image_url = r.json()["url"]
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        objective = objective.gen_update_with_an_image(image_filename, image_url)
        self.update_objective(objective)

    def upload_attachment_to_objective(
        self, headers: dict, objective: Objective, attachment_filename: str
    ):
        files = {"file": open(f"resources/attachments/{attachment_filename}", "rb")}
        attachment_url = ""
        if self.client is None:
            r = requests.post(
                self.file_url + objective.id + "/protected-files",
                files=files,
                headers=headers,
            )
            r.raise_for_status()
            attachment_url = r.json()["url"]
        else:
            with self.client.post(
                self.file_url + objective.id + "/protected-files",
                files=files,
                headers=headers,
                name="upload attachment to objective",
                catch_response=True,
            ) as response:
                if response.ok:
                    attachment_url = r.json()["url"]
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        objective = objective.gen_update_with_an_attachment(
            attachment_filename, attachment_url
        )
        self.update_objective(objective)
