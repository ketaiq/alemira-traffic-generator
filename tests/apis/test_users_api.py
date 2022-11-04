from app.apis.users_api import UsersAPI


def test_get_users_by_query():
    users_api = UsersAPI()
    data = users_api.get_users_by_query(0, 10)["data"]
    assert len(data) == 10


def main():
    test_get_users_by_query()


if __name__ == "__main__":
    main()
