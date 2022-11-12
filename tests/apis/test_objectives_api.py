from app.drivers.database_driver import db_driver
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.profiles.admin import Admin
from app.apis.objectives_api import ObjectivesAPI
import random
from app.models.objective.objective import Objective


def test_get_objectives_by_query():
    identity_api_endpoint = IdentityAPIEndPoint()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
    )
    objectives_api = ObjectivesAPI(db_driver)
    headers = admin._get_admin_headers()
    course_code = random.choice(db_driver.find_courses_codes())
    objective_dict = objectives_api.get_objectives_by_query(
        headers,
        {
            "requireTotalCount": True,
            "filter": f'["code","=","{course_code}"]',
        },
    )
    assert type(objective_dict) is dict


def test_download_attachment_from_objective():
    identity_api_endpoint = IdentityAPIEndPoint()
    admin = Admin(
        db_driver,
        identity_api_endpoint,
    )
    objectives_api = ObjectivesAPI(db_driver)
    headers = admin._get_admin_headers()
    objective_id = random.choice(db_driver.find_course_ids())
    assert type(objective_id) is str
    objective = objectives_api.get_objective_by_id(headers, objective_id)
    assert type(objective) is Objective
    if objective.has_attachment():
        res = objectives_api.download_attachment_from_objective(
            objective.get_attachment_url()
        )
        assert type(res) is str


def main():
    test_get_objectives_by_query()
    test_download_attachment_from_objective()


if __name__ == "__main__":
    main()
