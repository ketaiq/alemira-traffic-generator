from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.objectives_api import ObjectivesAPI
from app.models.objective.objective import Objective
from app.models.role import Role


def test_get_objective_by_id():
    identity_api_endpoint = IdentityAPIEndPoint()
    objectives_api = ObjectivesAPI(None)
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    objective = objectives_api.get_objective_by_id(
        headers, "2c513c25-4dc3-40fa-bcbd-0b06996023ed"
    )
    assert objective.code == "AAS310"


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


def test_get_objective_by_code_or_none():
    identity_api_endpoint = IdentityAPIEndPoint()
    objectives_api = ObjectivesAPI(None)
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    objective = objectives_api.get_objective_by_code_or_none(headers, "AAS310")
    assert objective.code == "AAS310"


def test_get_objective_personal_enrollments_by_query():
    identity_api_endpoint = IdentityAPIEndPoint()
    objectives_api = ObjectivesAPI(None)
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    res = objectives_api.get_objective_personal_enrollments_by_query(
        headers,
        "2c513c25-4dc3-40fa-bcbd-0b06996023ed",
        {
            "skip": 0,
            "take": 10,
            "requireTotalCount": True,
        },
    )
    assert len(res["data"]) <= res["totalCount"]


def test_get_objective_workflow_aggregate_by_id():
    identity_api_endpoint = IdentityAPIEndPoint()
    objectives_api = ObjectivesAPI(None)
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    res = objectives_api.get_objective_workflow_aggregate_by_id(
        headers, "2c513c25-4dc3-40fa-bcbd-0b06996023ed"
    )
    assert res["id"] == "3e4a8b5a-c2bd-4d7c-a67e-86c6b17e9981"
    assert "lastObjectiveRecord" in res
    assert "lastObjectiveWorkflow" in res


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
