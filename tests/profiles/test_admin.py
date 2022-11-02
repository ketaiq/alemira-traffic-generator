from app.profiles.admin import Admin
from app.drivers.database_driver import DatabaseDriver
from app.drivers.web_driver import WebDriver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI


def test_create_user():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    web_driver = WebDriver()
    lms_users_api = LmsUsersAPI(db_driver)
    mail_messages_api = MailMessagesAPI()
    account_reset_password_api = AccountResetPasswordAPI(db_driver, web_driver)
    admin = Admin(lms_users_api, mail_messages_api, account_reset_password_api)
    admin.create_user()


def main():
    test_create_user()


if __name__ == "__main__":
    main()
