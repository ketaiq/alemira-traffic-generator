import requests, logging
from app.apis.endpoint import EndPoint
from app.models.activity.activity import Activity
import pandas as pd
from app.drivers.database_driver import DatabaseDriver


class ActivitiesAPI(EndPoint):
    def __init__(self, driver: DatabaseDriver):
        super().__init__()
        self.url = self.uri + "activities/"
        self.driver = driver

    def get_activities(self) -> list[dict]:
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def create_random_activity(self, compositions_id: str, rich_text_id: str):
        new_activity = Activity.gen_random_object(
            compositions_id=compositions_id, rich_text_id=rich_text_id
        )
        r = requests.post(self.url, json=new_activity.to_dict(), headers=self.headers)
        r.raise_for_status()
        return r.json()

    def create_rich_text_courses(
        self, rich_text_id: str, course: pd.Series
    ) -> Activity:
        """
        Create courses from [1].
        [1]: https://waf.cs.illinois.edu/discovery/course-catalog.csv
        """

        course = Activity.gen_course(course, rich_text_id)
        r = requests.post(
            self.url, json=course.to_dict_for_creating(), headers=self.headers
        )
        r.raise_for_status()
        course.id = r.json()["id"]
        self.driver.insert_one_course(course.to_dict_for_database())
        return course


def main():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    activities_api = ActivitiesAPI(db_driver)
    activities = activities_api.get_activities()
    print(len(activities), " activities")


if __name__ == "__main__":
    main()
