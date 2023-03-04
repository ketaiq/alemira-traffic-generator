from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.users_api import UsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.objective_workflow_aggregates_api import ObjectiveWorkflowAggregatesAPI
from app.apis.activity_records_api import ActivityRecordsAPI
from app.apis.start_objective_workflows_api import StartObjectiveWorkflowsAPI
from app.apis.start_activity_workflows_api import StartActivityWorkflowsAPI
from app.apis.finish_activity_workflows_api import FinishActivityWorkflow
from app.apis.lms_users_api import LmsUsersAPI
from app.drivers.database_driver import db_driver
from app.models.role import Role
from app.models.user import User
from app.profiles.student import Student


def test_take_course():
    identity_api_endpoint = IdentityAPIEndPoint()
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    activity_records_api = ActivityRecordsAPI()
    start_objective_workflows_api = StartObjectiveWorkflowsAPI()
    start_activity_workflows_api = StartActivityWorkflowsAPI()
    student = Student(
        db_driver,
        identity_api_endpoint,
        users_api,
        lms_users_api,
        objectives_api,
        objective_workflow_aggregates_api,
        activity_records_api,
        start_objective_workflows_api,
        start_activity_workflows_api,
    )
    headers = student._get_student_headers()
    me = student.lms_users_api.get_user_me(headers)
    id = student._visit_one_course(headers, me)
    if id:
        res = student.objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
            headers, id
        )
    else:
        res = None
    assert id and res["lastObjectiveWorkflow"] is not None or id is None and res is None


def test_finish_one_course():
    # initialize the student object
    identity_api_endpoint = IdentityAPIEndPoint()
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    activity_records_api = ActivityRecordsAPI()
    start_objective_workflows_api = StartObjectiveWorkflowsAPI()
    start_activity_workflows_api = StartActivityWorkflowsAPI()
    finish_activity_workflows_api = FinishActivityWorkflow()
    student = Student(
        db_driver,
        identity_api_endpoint,
        users_api,
        lms_users_api,
        objectives_api,
        objective_workflow_aggregates_api,
        activity_records_api,
        start_objective_workflows_api,
        start_activity_workflows_api,
        finish_activity_workflows_api,
    )
    student.finish_one_course()


def test_start_one_course():
    # initialize the student object
    identity_api_endpoint = IdentityAPIEndPoint()
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    activity_records_api = ActivityRecordsAPI()
    start_objective_workflows_api = StartObjectiveWorkflowsAPI()
    start_activity_workflows_api = StartActivityWorkflowsAPI()
    finish_activity_workflows_api = FinishActivityWorkflow()
    student = Student(
        db_driver,
        identity_api_endpoint,
        users_api,
        lms_users_api,
        objectives_api,
        objective_workflow_aggregates_api,
        activity_records_api,
        start_objective_workflows_api,
        start_activity_workflows_api,
        finish_activity_workflows_api,
    )
    headers = student.identity_api_endpoint.get_headers(
        Role.STUDENT,
    )
    me = student.lms_users_api.get_user_me(headers)
    student._start_one_course(headers, me)


def test_review_one_course():
    # initialize the student object
    identity_api_endpoint = IdentityAPIEndPoint()
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    activity_records_api = ActivityRecordsAPI()
    start_objective_workflows_api = StartObjectiveWorkflowsAPI()
    start_activity_workflows_api = StartActivityWorkflowsAPI()
    finish_activity_workflows_api = FinishActivityWorkflow()
    student = Student(
        db_driver,
        identity_api_endpoint,
        users_api,
        lms_users_api,
        objectives_api,
        objective_workflow_aggregates_api,
        activity_records_api,
        start_objective_workflows_api,
        start_activity_workflows_api,
        finish_activity_workflows_api,
    )
    student.review_one_course()

def test_visit_my_courses():
    identity_api_endpoint = IdentityAPIEndPoint()
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI()
    activity_records_api = ActivityRecordsAPI()
    start_objective_workflows_api = StartObjectiveWorkflowsAPI()
    start_activity_workflows_api = StartActivityWorkflowsAPI()
    finish_activity_workflows_api = FinishActivityWorkflow()
    student = Student(
        db_driver,
        identity_api_endpoint,
        users_api,
        lms_users_api,
        objectives_api,
        objective_workflow_aggregates_api,
        activity_records_api,
        start_objective_workflows_api,
        start_activity_workflows_api,
        finish_activity_workflows_api,
    )
    student.visit_my_courses()


def main():
    # test_take_course()
    # test_finish_one_course()
    # test_start_one_course()
    # test_review_one_course()
    test_visit_my_courses()


if __name__ == "__main__":
    main()
