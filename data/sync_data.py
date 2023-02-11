from app.apis.lms_users_api import LmsUsersAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.profiles.admin import Admin
from app.drivers.database_driver import db_driver


def sync_local_data():
    """
    Synchronize data of users and courses in local mongodb with remote alemira database.
    """
    pass


def main():
    lms_users_api = LmsUsersAPI(db_driver)
    identity_api_endpoint = IdentityAPIEndPoint()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
    )
    headers = admin._get_admin_headers()
    lms_users_api.get_users_by_query(headers, {})


if __name__ == "__main__":
    main()
