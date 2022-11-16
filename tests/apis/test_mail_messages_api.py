from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.mail_messages_api import MailMessagesAPI
from app.models.role import Role


def test_get_mail_messages_by_query():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    mail_messages_api = MailMessagesAPI()
    res = mail_messages_api.get_mail_messages_by_query(
        headers, {"skip": 0, "take": 10, "requireTotalCount": True}
    )
    assert len(res["data"]) <= res["totalCount"]
