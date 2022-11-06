from app.apis.user_api_endpoint import UserAPIEndPoint
from app.drivers.database_driver import DatabaseDriver
from app.drivers.web_driver import WebDriver
from app.models.user import User
import requests
from app.utils.string import request_http_error_msg, request_timeout_msg


class AccountResetPasswordAPI(UserAPIEndPoint):
    def __init__(self, db_driver: DatabaseDriver, client=None):
        super().__init__(client)
        self.db_driver = db_driver

    def reset_password(
        self,
        url: str,
        user: User,
    ):
        if self.client is None:
            r = requests.get(url)
            r.raise_for_status()
        else:
            with self.client.get(
                url,
                name="visit reset password page",
                catch_response=True,
            ) as response:
                if not response.ok:
                    response.failure(request_http_error_msg(response))
                elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                    response.failure(request_timeout_msg())

        user.reset_password()
        web_driver = WebDriver()
        web_driver.reset_password(url, user)
        self.db_driver.update_password(user)
