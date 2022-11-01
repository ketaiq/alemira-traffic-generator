from app.profiles.admin import Admin
from app.database.driver import Driver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI


def test_create_user():
    driver = Driver("localhost:27017", "root", "rootpass")
    lms_users_api = LmsUsersAPI(driver)
    mail_messages_api = MailMessagesAPI()
    account_reset_password_api = AccountResetPasswordAPI(driver)
    admin = Admin(lms_users_api, mail_messages_api, account_reset_password_api)
    admin.create_user()


def main():
    test_create_user()


if __name__ == "__main__":
    main()
