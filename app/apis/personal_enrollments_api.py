from app.apis.user_api_endpoint import UserAPIEndPoint
from app.drivers.database_driver import DatabaseDriver
from app.models.personal_enrollment import PersonalEnrollment
import requests
from app.utils.string import request_timeout_msg, request_http_error_msg
from app.models.user import User
from app.utils.time import sleep_for_seconds


class PersonalEnrollmentsAPI(UserAPIEndPoint):
    def __init__(
        self,
        driver: DatabaseDriver,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "personal-enrollments/"
        self.driver = driver

    def create_personal_enrollment(
        self, headers: dict, objective_id: str, user_id: str
    ) -> PersonalEnrollment:
        personal_enrollment = PersonalEnrollment.gen_random_object(
            objective_id, user_id
        )
        if self.client is None:
            r = requests.post(
                self.url,
                json=personal_enrollment.to_dict_for_creating(),
                headers=headers,
            )
            r.raise_for_status()
            created_id = r.json()["id"]
            # check entity is created successfully
            for _ in range(10):
                created_state = self.get_created_personal_enrollment_state_by_id(
                    headers, created_id
                )
                if created_state["completed"]:
                    personal_enrollment.id = created_state["entityId"]
                    break
                sleep_for_seconds(1, 3)
        else:
            with self.client.post(
                self.url,
                json=personal_enrollment.to_dict_for_creating(),
                headers=headers,
                name="create personal enrollment",
                catch_response=True,
            ) as response:
                if response.ok:
                    created_id = response.json()["id"]
                    # check entity is created successfully
                    for _ in range(10):
                        created_state = (
                            self.get_created_personal_enrollment_state_by_id(
                                headers, created_id
                            )
                        )
                        if created_state["completed"]:
                            personal_enrollment.id = created_state["entityId"]
                            break
                        sleep_for_seconds(1, 3)
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        return personal_enrollment

    def get_created_personal_enrollment_state_by_id(
        self, headers: dict, id: str
    ) -> dict:
        if self.client is None:
            r = requests.get(
                self.uri + "create-personal-enrollments/" + id, headers=headers
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "create-personal-enrollments/" + id,
            headers=headers,
            name="get created personal enrollment state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_personal_enrollment_by_id(
        self, headers: dict, id: str
    ) -> PersonalEnrollment:
        if self.client is None:
            r = requests.get(self.url + id, headers=headers)
            r.raise_for_status()
            return PersonalEnrollment(r.json())
        with self.client.get(
            self.url + id,
            headers=headers,
            name="get personal enrollment by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return PersonalEnrollment(response.json())
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def delete_personal_enrollment_by_id(self, headers: dict, id: str):
        if self.client is None:
            r = requests.delete(self.url + id, headers=headers)
            r.raise_for_status()
            deleted_id = r.json()["id"]
            # check entity is deleted successfully
            for _ in range(10):
                deleted_state = self.get_deleted_personal_enrollment_state_by_id(
                    headers, deleted_id
                )
                if deleted_state["completed"]:
                    break
                sleep_for_seconds(1, 3)
        else:
            with self.client.delete(
                self.url + id,
                headers=headers,
                name="delete personal enrollment by id",
                catch_response=True,
            ) as response:
                if response.ok:
                    deleted_id = response.json()["id"]
                    # check entity is deleted successfully
                    for _ in range(10):
                        deleted_state = (
                            self.get_deleted_personal_enrollment_state_by_id(
                                headers, deleted_id
                            )
                        )
                        if deleted_state["completed"]:
                            break
                        sleep_for_seconds(1, 3)
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))

    def get_deleted_personal_enrollment_state_by_id(
        self, headers: dict, id: str
    ) -> dict:
        if self.client is None:
            r = requests.get(
                self.uri + "delete-personal-enrollments/" + id, headers=headers
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "delete-personal-enrollments/" + id,
            headers=headers,
            name="get deleted personal enrollment state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))
