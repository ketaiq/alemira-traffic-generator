import requests, logging
from app.apis.endpoint import EndPoint


class Users(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "users/"

    def get_user_objective_workflow_aggregates(self, id: str):
        r = requests.get(
            self.url + id + "/objective-workflow-aggregates/", headers=self.headers
        )
        r.raise_for_status()
        users = r.json()
        return users


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        filename="users_api.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    user_id = "dd3a261a-bcbe-4d35-a8a5-a9fc6e178bd3"
    users_api = Users()
    res = users_api.get_user_objective_workflow_aggregates(user_id)
    print(len(res))

    from app.models.objective.objective_workflow_aggregate import (
        ObjectiveWorkflowAggregate,
    )

    # print all courses for user
    for owa_dict in res:
        owa = ObjectiveWorkflowAggregate(owa_dict)
        print(owa.objective["name"])


if __name__ == "__main__":
    main()
