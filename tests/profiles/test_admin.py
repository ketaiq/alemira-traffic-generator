from app.profiles.admin import Admin
from app.drivers.database_driver import db_driver
from app.drivers.web_driver import WebDriver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI


def test_create_user():
    web_driver = WebDriver()
    lms_users_api = LmsUsersAPI(db_driver)
    num_users = len(lms_users_api.get_users())
    mail_messages_api = MailMessagesAPI()
    account_reset_password_api = AccountResetPasswordAPI(db_driver, web_driver)
    admin = Admin(lms_users_api, mail_messages_api, account_reset_password_api)
    admin._create_user()
    assert num_users + 1 == len(lms_users_api.get_users())


def main():
    test_create_user()


if __name__ == "__main__":
    main()
