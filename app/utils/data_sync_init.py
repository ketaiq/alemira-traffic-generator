from app.apis.datagrid_settings_api import DatagridSettingsAPI
from app.drivers.database_driver import db_driver
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.activities_api import ActivitiesAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.resource_libraries_api import ResourceLibrariesAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI
from app.apis.roles_api import RolesAPI
from app.apis.user_roles_api import UserRolesAPI
import pandas as pd
from app.models.activity.activity import Activity
from app.profiles.admin import Admin
import logging


def sync_local_data():
    """
    Synchronize data of users and courses in local mongodb with remote alemira database.
    """
    identity_api_endpoint = IdentityAPIEndPoint()
    lms_users_api = LmsUsersAPI(db_driver)
    mail_messages_api = MailMessagesAPI()
    account_reset_password_api = AccountResetPasswordAPI(db_driver)
    roles_api = RolesAPI()
    user_roles_api = UserRolesAPI()
    datagrid_settings_api = DatagridSettingsAPI()
    objectives_api = ObjectivesAPI(db_driver)
    activities_api = ActivitiesAPI(db_driver)
    admin = Admin(
        db_driver,
        identity_api_endpoint,
        lms_users_api,
        mail_messages_api,
        account_reset_password_api,
        roles_api,
        user_roles_api,
        datagrid_settings_api,
        activities_api,
        objectives_api,
    )
    admin.sync_local_users()
    admin.sync_local_activities()
    admin.sync_local_objectives()


def create_default_courses():
    identity_api_endpoint = IdentityAPIEndPoint()
    objectives_api = ObjectivesAPI(db_driver)
    activities_api = ActivitiesAPI(db_driver)
    resource_libraries_api = ResourceLibrariesAPI()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
        activities_api=activities_api,
        objectives_api=objectives_api,
        resource_libraries_api=resource_libraries_api,
    )
    df = pd.read_csv("data/course-catalog.csv")
    for index in df.index:
        activity = admin.create_activity_if_not_exists(
            df.loc[index, "Code"], df.loc[index]
        )
        admin.create_objective_if_not_exists(activity)


def create_default_users():
    identity_api_endpoint = IdentityAPIEndPoint()
    lms_users_api = LmsUsersAPI(db_driver)
    mail_messages_api = MailMessagesAPI()
    account_reset_password_api = AccountResetPasswordAPI(db_driver)
    roles_api = RolesAPI()
    user_roles_api = UserRolesAPI()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
        lms_users_api,
        mail_messages_api,
        account_reset_password_api,
        roles_api,
        user_roles_api,
    )
    for _ in range(100):
        admin.create_student_user()
    for _ in range(20):
        admin.create_instructor_user()


def main():
    logging.basicConfig(
        filename="data_sync_init.log",
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )
    sync_local_data()
    # create_default_courses()
    create_default_users()


if __name__ == "__main__":
    main()
