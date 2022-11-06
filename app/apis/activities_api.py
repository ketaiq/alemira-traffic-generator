import requests, logging
from app.apis.user_api_endpoint import UserAPIEndPoint
from app.models.activity.activity import Activity
from app.models.user import User
import pandas as pd
from app.drivers.database_driver import DatabaseDriver
from app.utils.string import request_timeout_msg, request_http_error_msg


class ActivitiesAPI(UserAPIEndPoint):
    def __init__(
        self,
        driver: DatabaseDriver,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "activities/"
        self.driver = driver

    def get_activities(self, headers: dict) -> list[dict]:
        r = requests.get(self.url, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_activities_by_query(self, headers: dict, query: dict) -> dict:
        if self.client is None:
            r = requests.get(self.url + "query", headers=headers, params=query)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "query",
            headers=headers,
            params=query,
            name="get activities by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_activity_by_code_or_none(self, headers: dict, code: str) -> Activity | None:
        # TODO use = compare directly in query
        skip = 0
        take = 10
        while True:
            res = self.get_activities_by_query(
                headers, {"skip": skip, "take": take, "requireTotalCount": True}
            )
            remaining_count = res["totalCount"] - take - skip
            activity = next(
                (activity for activity in res["data"] if activity["code"] == code),
                None,
            )
            skip += take
            if activity is not None:
                return Activity(activity)
            if remaining_count <= 0:
                break
        return None

    def get_created_activity_state_by_id(self, headers: dict, created_id: str):
        if self.client is None:
            r = requests.get(
                self.uri + "create-lms-users/" + created_id, headers=headers
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "create-activities/" + created_id,
            headers=headers,
            name="get created activity state by id",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def get_updated_activity_state_by_id(self, headers: dict, update_id: str) -> dict:
        if self.client is None:
            r = requests.get(
                self.uri + "update-activities/" + update_id, headers=headers
            )
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.uri + "update-activities/" + update_id,
            headers=headers,
            name="get updated activity",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))

    def update_activity(self, headers: dict, activity: Activity) -> str:
        if self.client is None:
            r = requests.put(
                self.url + activity.id,
                json=activity.to_dict_for_updating(),
                headers=headers,
            )
            r.raise_for_status()
            self.driver.update_course(activity)
            return r.json()["id"]
        else:
            with self.client.put(
                self.url + activity.id,
                json=activity.to_dict_for_updating(),
                headers=headers,
                name="update activity",
                catch_response=True,
            ) as response:
                if response.ok:
                    self.driver.update_course(activity)
                    return response.json()["id"]
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())
                else:
                    response.failure(request_http_error_msg(response))

    def create_random_activity(
        self, headers: dict, compositions_id: str, rich_text_id: str
    ):
        new_activity = Activity.gen_random_object(
            compositions_id=compositions_id, rich_text_id=rich_text_id
        )
        r = requests.post(
            self.url, json=new_activity.to_dict_for_creating(), headers=headers
        )
        r.raise_for_status()
        return r.json()

    def create_rich_text_courses(
        self, headers: dict, rich_text_id: str, course_series: pd.Series
    ) -> Activity:
        course = Activity.gen_course(course_series, rich_text_id)
        r = requests.post(self.url, json=course.to_dict_for_creating(), headers=headers)
        r.raise_for_status()
        course.id = self.get_created_activity_state_by_id(headers, r.json()["id"])[
            "entityId"
        ]
        self.driver.insert_one_course(course)
        return course
