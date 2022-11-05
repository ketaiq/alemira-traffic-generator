import requests, logging
from app.apis.endpoint import EndPoint
from app.utils.string import request_timeout_msg, request_http_error_msg
from app.models.user import User


class UsersAPI(EndPoint):
    def __init__(
        self,
        role: str = "admin",
        user: User = None,
        client=None,
    ):
        super().__init__(role, user, client)
        self.url = self.uri + "users/"

    def get_user_objective_workflow_aggregates(self, id: str):
        r = requests.get(
            self.url + id + "/objective-workflow-aggregates/", headers=self.headers
        )
        r.raise_for_status()
        users = r.json()
        return users

    def get_users_by_query(self, query: dict) -> dict:
        if self.client is None:
            r = requests.get(self.url + "query", headers=self.headers, params=query)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "query",
            headers=self.headers,
            params=query,
            name="get users by query",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        filename="users_api.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    user_id = "dd3a261a-bcbe-4d35-a8a5-a9fc6e178bd3"
    users_api = UsersAPI()
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
