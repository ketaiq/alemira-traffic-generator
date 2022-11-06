from app.drivers.database_driver import DatabaseDriver
from app.apis.activities_api import ActivitiesAPI


def test_get_activities_by_query():
    # TODO use headers
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    activities_api = ActivitiesAPI(db_driver)
    headers = {}
    query = {"skip": 0, "take": 10, "requireTotalCount": True}
    res = activities_api.get_activities_by_query(headers, query)
    assert len(res["data"]) == 10
    assert res["totalCount"] > 0


def main():
    test_get_activities_by_query()


if __name__ == "__main__":
    main()
