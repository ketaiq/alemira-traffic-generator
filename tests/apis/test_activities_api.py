from app.drivers.database_driver import db_driver
from app.apis.activities_api import ActivitiesAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.models.role import Role


def test_get_activities():
    activities_api = ActivitiesAPI(db_driver)
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    activities = activities_api.get_activities(headers)
    assert len(activities) >= 0


def test_get_activities_by_query():
    activities_api = ActivitiesAPI(db_driver)
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    query = {"skip": 0, "take": 10, "requireTotalCount": True}
    res = activities_api.get_activities_by_query(headers, query)
    assert len(res["data"]) <= 10
    assert res["totalCount"] >= 0


def main():
    test_get_activities_by_query()


if __name__ == "__main__":
    main()
