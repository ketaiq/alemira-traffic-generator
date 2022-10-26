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

    def create_activity(self):
        new_activity = Activity.gen_random_object()
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
    activities_api.create_activity()
    activities = activities_api.get_activities()
    print(len(activities), " activities")


if __name__ == "__main__":
    main()
