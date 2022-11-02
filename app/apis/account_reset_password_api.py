from app.apis.endpoint import EndPoint
from app.drivers.database_driver import DatabaseDriver
from app.drivers.web_driver import WebDriver
from app.models.user import User


class AccountResetPasswordAPI(EndPoint):
    def __init__(self, db_driver: DatabaseDriver, web_driver: WebDriver):
        self.headers = {
            "accept": "*/*",
        }
        self.db_driver = db_driver
        self.web_driver = web_driver

    def reset_password(
        self,
        url: str,
        user: User,
    ):
        user.reset_password()
        self.web_driver.reset_password(url, user)
        self.db_driver.update_password(user)
