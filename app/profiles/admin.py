import logging, random
from app.utils.time import sleep_for_seconds
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI
from app.exceptions import MailNotFoundException
from app.models.mail_message import MailMessage
from app.apis.roles_api import RolesAPI
from app.models.user import User
from app.apis.user_roles_api import UserRolesAPI
from app.exceptions import RoleNotFoundException
from app.models.role import Role
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.drivers.database_driver import DatabaseDriver


class Admin:
    """A class to represent the profile of administrators."""

    def __init__(
        self,
        db_driver: DatabaseDriver,
        identity_api_endpoint: IdentityAPIEndPoint,
        lms_users_api: LmsUsersAPI,
        mail_messages_api: MailMessagesAPI,
        account_reset_password_api: AccountResetPasswordAPI,
        roles_api: RolesAPI,
        user_roles_api: UserRolesAPI,
    ):
        self.db_driver = db_driver
        self.identity_api_endpoint = identity_api_endpoint
        self.lms_users_api = lms_users_api
        self.mail_messages_api = mail_messages_api
        self.account_reset_password_api = account_reset_password_api
        self.roles_api = roles_api
        self.user_roles_api = user_roles_api

    def select_one_admin(self) -> User:
        return User(random.choice(self.db_driver.find_all_admin_users()))

    def _get_admin_headers(self) -> dict:
        return self.identity_api_endpoint.get_headers(
            Role.ADMIN, self.select_one_admin()
        )

    def get_num_of_users(self) -> int:
        headers = self._get_admin_headers()
        return self.lms_users_api.get_users_by_query(
            headers, {"skip": 0, "take": 1, "requireTotalCount": True}
        )["totalCount"]

    def _create_user(self, headers: dict, role: Role) -> User:
        """Create a user with a random profile."""
        new_user = self.lms_users_api.create_user(headers, role)
        sleep_for_seconds(20, 30)
        skip = 0
        take = 10
        try:
            while True:
                res = self.mail_messages_api.get_mail_messages_by_query(
                    headers, {"skip": skip, "take": take, "requireTotalCount": True}
                )
                remaining_count = res["totalCount"] - take - skip
                mail_messages = [MailMessage(msg) for msg in res["data"]]
                mail = next(
                    (mail for mail in mail_messages if mail.is_sent_to_user(new_user)),
                    None,
                )
                skip += take
                if mail is not None:
                    url = mail.get_reset_password_url()
                    self.account_reset_password_api.reset_password(url, new_user)
                    break
                if remaining_count <= 0:
                    raise MailNotFoundException(
                        f"No mail is sent to user {new_user.username}."
                    )
            return new_user
        except MailNotFoundException as e:
            logging.error(e.message)

    def create_user(self, role: Role):
        headers = self._get_admin_headers()
        user = self._create_user(headers, role)
        roles = self.roles_api.get_roles_by_query(
            headers,
            {"requireTotalCount": True, "filter": f'["name","=","{role.value}"]'},
        )
        try:
            if roles["totalCount"] > 0:
                self.user_roles_api.create_user_role(
                    headers, user.id, roles["data"][0]["id"]
                )
            else:
                raise RoleNotFoundException(f"Role {role.value} doesn't exist.")
        except RoleNotFoundException as e:
            logging.error(e.message)

    def create_admin_user(self):
        self.create_user(Role.ADMIN)

    def create_instructor_user(self):
        self.create_user(Role.INSTRUCTOR)

    def create_student_user(self):
        self.create_user(Role.STUDENT)
