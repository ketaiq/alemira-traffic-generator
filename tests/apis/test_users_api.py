from app.apis.users_api import UsersAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.models.role import Role


def test_get_users_by_query():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    users_api = UsersAPI()
    data = users_api.get_users_by_query(
        headers, {"skip": 0, "take": 10, "requireTotalCount": True}
    )["data"]
    assert len(data) >= 0 and len(data) <= 10


def main():
    test_get_users_by_query()


if __name__ == "__main__":
    main()
