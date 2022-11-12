from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.models.user import User
from app.models.role import Role


def test_identity_api_endpoint():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    assert len(headers["Authorization"]) > len("Bearer ")


def main():
    test_identity_api_endpoint()


if __name__ == "__main__":
    main()
