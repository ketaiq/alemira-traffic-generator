from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.user_roles_api import UserRolesAPI
from app.models.role import Role


def test_get_user_roles_by_query():
    user_id = "b9aeb6d4-c784-4c2d-a216-e8fff0e93bcc"
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    user_roles_api = UserRolesAPI()
    res = user_roles_api.get_user_roles_by_query(
        headers,
        {
            "requireTotalCount": True,
            "filter": f'["user.id","=","{user_id}"]',
        },
    )
    assert len(res.get("data")) != 0


if __name__ == "__main__":
    test_get_user_roles_by_query()
