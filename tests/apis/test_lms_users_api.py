from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.lms_users_api import LmsUsersAPI
from app.models.role import Role
from app.models.user import User


def test_get_user_me():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    lms_users_api = LmsUsersAPI(None)
    me = lms_users_api.get_user_me(headers)
    assert type(me) is User
    assert me.email == "alice@company.com"


def test_get_users():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    lms_users_api = LmsUsersAPI(None)
    users = lms_users_api.get_users(headers)
    assert len(users) > 0


def test_get_user_by_id():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    lms_users_api = LmsUsersAPI(None)
    user = lms_users_api.get_user_by_id(headers, "dd3a261a-bcbe-4d35-a8a5-a9fc6e178bd3")
    assert type(user) is User
    assert user.id == "dd3a261a-bcbe-4d35-a8a5-a9fc6e178bd3"
    assert user.email == "alice@company.com"


def test_get_users_by_query():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    lms_users_api = LmsUsersAPI(None)
    res = lms_users_api.get_users_by_query(
        headers,
        {
            "skip": 0,
            "take": 10,
            "requireTotalCount": True,
            "filter": '["email","contains","alice"]',
        },
    )
    assert len(res["data"]) == res["totalCount"]
    assert "alice" in res["data"][0]["email"]
