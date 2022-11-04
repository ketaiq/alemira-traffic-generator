from app.apis.endpoint import EndPoint
from app.drivers.database_driver import DatabaseDriver
from app.models.personal_enrollment import PersonalEnrollment
import requests
from app.utils.string import request_timeout_msg, request_http_error_msg


class PersonalEnrollmentsAPI(EndPoint):
    def __init__(self, driver: DatabaseDriver):
        super().__init__()
        self.url = self.uri + "personal-enrollments/"
        self.driver = driver

    def create_personal_enrollment(self, objective_id: str, user_id: str, client=None) -> PersonalEnrollment:
        personal_enrollment = PersonalEnrollment.gen_random_object(
            objective_id, user_id
        )
        if client is None:
            r = requests.post(
                self.url,
                json=personal_enrollment.to_dict_for_creating(),
                headers=self.headers,
            )
            r.raise_for_status()
            personal_enrollment.id = r.json()["id"]
        else:
            with client.post(
                self.url,
                json=personal_enrollment.to_dict_for_creating(),
                headers=self.headers,
                name="create personal enrollment",
                catch_response=True,
            ) as response:
                if response.ok:
                    personal_enrollment.id = response.json()["id"]
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))
        return personal_enrollment
