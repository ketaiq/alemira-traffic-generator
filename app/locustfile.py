from locust import HttpUser, task, between
from app.profiles.admin import Admin
from app.drivers.database_driver import db_driver
from app.drivers.web_driver import WebDriver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI
from app.apis.roles_api import RolesAPI
from app.apis.user_roles_api import UserRolesAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint


class AdminUser(HttpUser):
    weight = 1
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        identity_api_endpoint = IdentityAPIEndPoint(client=self.client)
        lms_users_api = LmsUsersAPI(db_driver, client=self.client)
        mail_messages_api = MailMessagesAPI(client=self.client)
        account_reset_password_api = AccountResetPasswordAPI(
            db_driver, self.client
        )
        roles_api = RolesAPI(client=self.client)
        user_roles_api = UserRolesAPI(client=self.client)
        self.admin = Admin(
            identity_api_endpoint,
            lms_users_api,
            mail_messages_api,
            account_reset_password_api,
            roles_api,
            user_roles_api,
        )
        # use specific url for each request
        self.client.base_url = ""

    @task(100)
    def get_users(self):
        self.admin.lms_users_api.get_users()

    @task(1)
    def create_admin_user(self):
        self.admin.create_admin_user()

    @task(5)
    def create_instructor_user(self):
        self.admin.create_instructor_user()

    @task(40)
    def create_student_user(self):
        self.admin.create_student_user()


class StudentUser(HttpUser):
    weight = 20
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.student = Student(
        #     lms_users_api, mail_messages_api, account_reset_password_api
        # )
        # use specific url for each request
        self.client.base_url = ""
