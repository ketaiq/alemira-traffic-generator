from app.drivers.database_driver import db_driver
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.profiles.admin import Admin
from app.apis.objectives_api import ObjectivesAPI


def test_get_objectives_by_query():
    identity_api_endpoint = IdentityAPIEndPoint()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
    )
    objectives_api = ObjectivesAPI(db_driver)
    headers = admin._get_admin_headers()
    for course_code in db_driver.find_courses_codes():
        objective_dict = objectives_api.get_objectives_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["code","=","{course_code}"]',
            },
        )
        assert objective_dict is not None


def main():
    test_get_objectives_by_query()


if __name__ == "__main__":
    main()
