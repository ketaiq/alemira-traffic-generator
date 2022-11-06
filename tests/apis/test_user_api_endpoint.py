from app.apis.user_api_endpoint import UserAPIEndPoint
from app.models.user import User


def test_user_api_endpoint():
    user = User(username="6t2.Kuq8FDZT5T@T.uM.wJndp", password="tW5$lA")
    ep = UserAPIEndPoint(user)
    assert len(ep.headers["Authorization"]) > len("Bearer ")


def main():
    test_user_api_endpoint()


if __name__ == "__main__":
    main()
