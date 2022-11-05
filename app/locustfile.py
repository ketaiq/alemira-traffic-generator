from locust import HttpUser, task, between
from app.profiles.admin import Admin
from app.drivers.database_driver import db_driver
from app.drivers.web_driver import web_driver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI


class AdminUser(HttpUser):
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lms_users_api = LmsUsersAPI(db_driver, client=self.client)
        mail_messages_api = MailMessagesAPI(client=self.client)
        account_reset_password_api = AccountResetPasswordAPI(db_driver, web_driver)
        self.admin = Admin(lms_users_api, mail_messages_api, account_reset_password_api)
        # use specific url for each request
        self.client.base_url = ""

    @task
    def get_users(self):
        self.admin.lms_users_api.get_users()
