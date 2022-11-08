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


def test_download_attachment_from_objective():
    identity_api_endpoint = IdentityAPIEndPoint()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
    )
    objectives_api = ObjectivesAPI(db_driver)
    headers = admin._get_admin_headers()
    for objective_id in db_driver.find_course_ids():
        objective = objectives_api.get_objective_by_id(headers, objective_id)
        if objective.has_attachment():
            objectives_api.download_attachment_from_objective(
                objective.get_attachment_url()
            )


def main():
    # test_get_objectives_by_query()
    test_download_attachment_from_objective()


if __name__ == "__main__":
    main()
