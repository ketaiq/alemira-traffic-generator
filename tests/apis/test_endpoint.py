from app.apis.endpoint import EndPoint
from app.models.user import User


def test_endpoint():
    user = User(username="6t2.Kuq8FDZT5T@T.uM.wJndp", password="tW5$lA")
    ep = EndPoint(user)
    assert len(ep.headers["Authorization"]) > len("Bearer ")


def main():
    test_endpoint()


if __name__ == "__main__":
    main()
