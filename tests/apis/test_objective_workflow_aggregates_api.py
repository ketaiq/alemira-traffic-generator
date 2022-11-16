from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.objective_workflow_aggregates_api import ObjectiveWorkflowAggregatesAPI
from app.models.role import Role


def test_get_objective_workflow_aggregate_by_id():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    owa = objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
        headers, "3e4a8b5a-c2bd-4d7c-a67e-86c6b17e9981"
    )
    assert owa["id"] == "3e4a8b5a-c2bd-4d7c-a67e-86c6b17e9981"
    assert owa["objective"] is not None


def test_get_objective_records_by_id():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    owa_records = objective_workflow_aggregates_api.get_objective_records_by_id(
        headers, "3e4a8b5a-c2bd-4d7c-a67e-86c6b17e9981"
    )
    assert type(owa_records) is list
    assert len(owa_records) > 0


def test_get_activity_with_aggregates_by_id():
    identity_api_endpoint = IdentityAPIEndPoint()
    headers = identity_api_endpoint.get_headers(Role.ADMIN)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    res = objective_workflow_aggregates_api.get_activity_with_aggregates_by_id(
        headers,
        "3e4a8b5a-c2bd-4d7c-a67e-86c6b17e9981",
        "cb1fdf87-ef7e-46d9-951d-64aa068cb960",
    )
    assert res["code"] == "AAS310"
