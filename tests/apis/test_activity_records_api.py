from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.activity_records_api import ActivityRecordsAPI
from app.models.role import Role


def test_get_activity_records_by_query():
    activity_records_api = ActivityRecordsAPI()
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    res = activity_records_api.get_activity_records_by_query(
        headers,
        {
            "requireTotalCount": True,
            "filter": f'[["activity.id","=","e45e9bb5-8adf-438c-a1a4-e6971eff278b"],"and",["user.id","=","dd3a261a-bcbe-4d35-a8a5-a9fc6e178bd3"]]',
        },
    )
    assert type(res) is dict
    assert len(res["data"]) == res["totalCount"]


def main():
    test_get_activity_records_by_query()


if __name__ == "__main__":
    main()
