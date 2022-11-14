from app.apis.activities_api import ActivitiesAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.models.role import Role
from app.models.activity.activity import Activity
from app.utils.string import gen_random_description


def test_get_activities():
    activities_api = ActivitiesAPI(None)
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    activities = activities_api.get_activities(headers)
    assert len(activities) >= 0


def test_get_activities_by_query():
    activities_api = ActivitiesAPI(None)
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    query = {"skip": 0, "take": 10, "requireTotalCount": True}
    res = activities_api.get_activities_by_query(headers, query)
    assert len(res["data"]) <= 10
    assert res["totalCount"] >= 0


def test_update_activity():
    activities_api = ActivitiesAPI(None)
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    res = activities_api.get_activities_by_query(
        headers,
        {
            "requireTotalCount": True,
            "filter": f'["code","=","AAS246"]',
        },
    )
    activity_to_update = Activity(res["data"][0])
    activity_to_update.description = gen_random_description()
    activities_api.update_activity(headers, activity_to_update)


def main():
    # test_get_activities_by_query()
    test_update_activity()


if __name__ == "__main__":
    main()
