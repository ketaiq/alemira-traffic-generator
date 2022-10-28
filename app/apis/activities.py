import requests, logging
from app.apis.endpoint import EndPoint
from app.models.activity.activity import Activity


class Activities(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "activities/"

    def get_activities(self) -> list[dict]:
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def create_activity(self, compositions_id: str, rich_text_id: str):
        new_activity = Activity.gen_random_object(
            compositions_id=compositions_id, rich_text_id=rich_text_id
        )
        r = requests.post(self.url, json=new_activity.to_dict(), headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")


def main():
    activities_api = Activities()

    activities = activities_api.get_activities()
    print(len(activities), " activities")

    from app.apis.resource_libraries import ResourceLibraries

    resource_libraries_api = ResourceLibraries()
    compositions_id = resource_libraries_api.get_compositions_id()
    rich_text_id = resource_libraries_api.get_rich_text_id()
    print(activities_api.create_activity(compositions_id, rich_text_id))
    activities = activities_api.get_activities()
    print(len(activities), " activities")


if __name__ == "__main__":
    main()
