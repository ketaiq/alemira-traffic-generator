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
from app.profiles.admin import Admin


def create_default_courses():
    identity_api_endpoint = IdentityAPIEndPoint()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
    )
    objectives_api = ObjectivesAPI(db_driver)
    activities_api = ActivitiesAPI(db_driver)
    resource_libraries_api = ResourceLibrariesAPI()
    headers = admin._get_admin_headers()
    rich_text_id = resource_libraries_api.get_rich_text_id(headers)
    df = pd.read_csv("data/course-catalog.csv")
    for index in df.index[0:5]:
        # check if course exists
        course = activities_api.get_activity_by_code_or_none(
            headers, df.loc[index, "Code"]
        )
        if course is None:
            course = activities_api.create_rich_text_courses(
                headers, rich_text_id, df.loc[index]
            )
        elif db_driver.check_activity_by_code(course):
            db_driver.update_activity(course)
        else:
            db_driver.insert_one_activity(course)
        # check if objective exists
        objective = objectives_api.get_objective_by_code_or_none(headers, course.code)
        if objective is None:
            update_id = activities_api.update_activity(headers, course)
            created_id = objectives_api.create_objective(headers, course)
            while True:
                updated_status = activities_api.get_updated_activity_state_by_id(
                    headers, update_id
                )
                created_status = objectives_api.get_created_objective_state_by_id(
                    headers, created_id
                )
                if (
                    updated_status["completed"] is not None
                    and created_status["completed"] is not None
                ):
                    break
        elif db_driver.check_objective_by_code(objective):
            db_driver.update_objective(objective)
        else:
            db_driver.insert_one_objective(objective)


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
    for _ in range(10):
        admin.create_student_user()
    for _ in range(2):
        admin.create_instructor_user()


def main():
    create_default_courses()
    create_default_users()


if __name__ == "__main__":
    main()
