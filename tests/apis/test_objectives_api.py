from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.objectives_api import ObjectivesAPI
from app.models.objective.objective import Objective
from app.models.role import Role


def test_get_objectives_by_query():
    identity_api_endpoint = IdentityAPIEndPoint()
    objectives_api = ObjectivesAPI(None)
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    course_code = "03.09-2"
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
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    objectives_api = ObjectivesAPI(None)
    objective_id = "d83fbac3-bcf0-4a0f-ad1a-6d6c4dbde6ed"
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
