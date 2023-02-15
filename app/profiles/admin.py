import logging, random
import pandas as pd
from app.utils.string import gen_default_password
from app.utils.time import sleep_for_seconds
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI
from app.exceptions.required_object_not_found import MailNotFoundException
from app.exceptions.required_object_not_found import RoleNotFoundException
from app.models.mail_message import MailMessage
from app.apis.roles_api import RolesAPI
from app.models.user import User
from app.apis.user_roles_api import UserRolesAPI
from app.models.role import Role
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.drivers.database_driver import DatabaseDriver
from app.apis.datagrid_settings_api import DatagridSettingsAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.activities_api import ActivitiesAPI
from app.models.activity.activity import Activity
from app.models.objective.objective import Objective
from app.apis.resource_libraries_api import ResourceLibrariesAPI


class Admin:
    """A class to represent the profile of administrators."""

    def __init__(
        self,
        db_driver: DatabaseDriver,
        identity_api_endpoint: IdentityAPIEndPoint,
        lms_users_api: LmsUsersAPI = None,
        mail_messages_api: MailMessagesAPI = None,
        account_reset_password_api: AccountResetPasswordAPI = None,
        roles_api: RolesAPI = None,
        user_roles_api: UserRolesAPI = None,
        datagrid_settings_api: DatagridSettingsAPI = None,
        activities_api: ActivitiesAPI = None,
        objectives_api: ObjectivesAPI = None,
        resource_libraries_api: ResourceLibrariesAPI = None,
    ):
        self.db_driver = db_driver
        self.identity_api_endpoint = identity_api_endpoint
        self.lms_users_api = lms_users_api
        self.mail_messages_api = mail_messages_api
        self.account_reset_password_api = account_reset_password_api
        self.roles_api = roles_api
        self.user_roles_api = user_roles_api
        self.datagrid_settings_api = datagrid_settings_api
        self.activities_api = activities_api
        self.objectives_api = objectives_api
        self.resource_libraries_api = resource_libraries_api

    def get_num_of_users(self) -> int:
        headers = self._get_admin_headers()
        return self.lms_users_api.get_users_by_query(
            headers, {"skip": 0, "take": 1, "requireTotalCount": True}
        )["totalCount"]

    def get_datagrid_tenants(self) -> dict:
        headers = self._get_admin_headers()
        return self.datagrid_settings_api.get_datagrid_tenants(headers)

    def create_admin_user(self):
        self.create_user(Role.ADMIN)

    def create_instructor_user(self):
        self.create_user(Role.INSTRUCTOR)

    def create_student_user(self):
        self.create_user(Role.STUDENT)

    def _create_user(self, headers: dict, role: Role) -> User:
        """Create a user with a random profile."""
        new_user = self.lms_users_api.create_user(headers, role)
        sleep_for_seconds(20, 30)
        try:
            res = self.mail_messages_api.get_mail_messages_by_query(
                headers,
                {
                    "requireTotalCount": True,
                    "filter": f'["toAddress","=","{new_user.email}"]',
                },
            )
            if len(res) > 0:
                mail = MailMessage(res["data"][0])
                url = mail.get_reset_password_url()
                self.account_reset_password_api.reset_password(url, new_user)
            else:
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

    def sync_local_users(self):
        """Synchronize users in local mongodb with remote alemira database."""
        headers = self._get_admin_headers()
        skip = 0
        take = 10
        while True:
            res = self.lms_users_api.get_users_by_query(
                headers, {"skip": skip, "take": take, "requireTotalCount": True}
            )
            remaining_count = res["totalCount"] - take - skip
            users = res["data"]
            users = User.filter_original_users(users)
            for user in users:
                user = User(user)
                if not self.db_driver.check_user_by_id(user):
                    user_student_roles = self.user_roles_api.get_user_roles_by_query(
                        headers,
                        {
                            "requireTotalCount": True,
                            "filter": f'[["user.id","=","{user.id}"],"and",["role.name","=","{Role.STUDENT.value}"]]',
                        },
                    )
                    user_instructor_roles = self.user_roles_api.get_user_roles_by_query(
                        headers,
                        {
                            "requireTotalCount": True,
                            "filter": f'[["user.id","=","{user.id}"],"and",["role.name","=","{Role.INSTRUCTOR.value}"]]',
                        },
                    )
                    if len(user_instructor_roles) != 0:
                        user._role = Role.INSTRUCTOR.value
                    elif len(user_student_roles) != 0:
                        user._role = Role.STUDENT.value
                    else:
                        user._role = "Unknown"
                    user.password = gen_default_password()
                    self.db_driver.insert_one_user(user)
            skip += take
            if remaining_count <= 0:
                break

    def sync_local_activities(self):
        """Synchronize activities in local mongodb with remote alemira database."""
        headers = self._get_admin_headers()
        skip = 0
        take = 10
        while True:
            res = self.activities_api.get_activities_by_query(
                headers, {"skip": skip, "take": take, "requireTotalCount": True}
            )
            remaining_count = res["totalCount"] - take - skip
            activities = res["data"]
            activities = Activity.filter_original_activities(activities)
            for activity in activities:
                activity = Activity(activity)
                if not self.db_driver.check_activity_by_code(activity):
                    self.db_driver.insert_one_activity(activity)
            skip += take
            if remaining_count <= 0:
                break

    def sync_local_objectives(self):
        """Synchronize objectives in local mongodb with remote alemira database."""
        headers = self._get_admin_headers()
        skip = 0
        take = 10
        while True:
            res = self.objectives_api.get_objectives_by_query(
                headers, {"skip": skip, "take": take, "requireTotalCount": True}
            )
            remaining_count = res["totalCount"] - take - skip
            objectives = res["data"]
            objectives = Objective.filter_original_objectives(objectives)
            for objective in objectives:
                objective = Objective(objective)
                if not self.db_driver.check_objective_by_code(objective):
                    self.db_driver.insert_one_objective(objective)
            skip += take
            if remaining_count <= 0:
                break

    def _select_one_admin(self) -> User:
        return User(random.choice(self.db_driver.find_admin_users()))

    def _get_admin_headers(self) -> dict:
        return self.identity_api_endpoint.get_headers(Role.ADMIN)

    def create_activity_if_not_exists(
        self, code: str, course_series: pd.Series
    ) -> Activity:
        headers = self._get_admin_headers()
        rich_text_id = self.resource_libraries_api.get_rich_text_id(headers)
        # check if activity exists
        res = self.activities_api.get_activities_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["code","=","{code}"]',
            },
        )
        if len(res["data"]) == 0:
            activity = self.activities_api.create_rich_text_courses(
                headers, rich_text_id, course_series
            )
        else:
            activity = Activity(res["data"][0])
            if self.db_driver.check_activity_by_code(activity):
                self.db_driver.update_activity(activity)
            else:
                self.db_driver.insert_one_activity(activity)
        return activity

    def create_objective_if_not_exists(self, activity: Activity):
        headers = self._get_admin_headers()
        # check if objective exists
        res = self.objectives_api.get_objectives_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["code","=","{activity.code}"]',
            },
        )
        if len(res["data"]) == 0:
            self.activities_api.update_activity(headers, activity)
            self.objectives_api.create_objective(headers, activity)
        else:
            objective = Objective(res["data"][0])
            if self.db_driver.check_objective_by_code(objective):
                self.db_driver.update_objective(objective)
            else:
                self.db_driver.insert_one_objective(objective)
