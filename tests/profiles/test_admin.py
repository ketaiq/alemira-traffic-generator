from app.profiles.admin import Admin
from app.drivers.database_driver import db_driver
from app.drivers.web_driver import WebDriver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.roles_api import RolesAPI
from app.apis.user_roles_api import UserRolesAPI
from app.models.user import User
from app.models.role import Role


def test_create_admin_user():
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
    num_users = admin.get_num_of_users()
    admin.create_admin_user()
    assert num_users + 1 == admin.get_num_of_users()


def test_create_instructor_user():
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
    num_users = admin.get_num_of_users()
    admin.create_instructor_user()
    assert num_users + 1 == admin.get_num_of_users()


def test_create_student_user():
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
    num_users = admin.get_num_of_users()
    admin.create_student_user()
    assert num_users + 1 == admin.get_num_of_users()


def test_select_one_admin():
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
    user = admin._select_one_admin()
    assert type(user) is User
    assert user._role == Role.ADMIN.value


def main():
    # test_create_user()
    # test_select_one_admin()
    # test_create_admin_user()
    test_create_instructor_user()
    test_create_student_user()


if __name__ == "__main__":
    main()
