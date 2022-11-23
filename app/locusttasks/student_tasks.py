import logging
from app.drivers.database_driver import db_driver
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.objective_workflow_aggregates_api import ObjectiveWorkflowAggregatesAPI
from app.apis.activity_records_api import ActivityRecordsAPI
from app.apis.start_objective_workflows_api import StartObjectiveWorkflowsAPI
from app.apis.start_activity_workflows_api import StartActivityWorkflowsAPI
from app.apis.finish_activity_workflows_api import FinishActivityWorkflow
from app.profiles.student import Student

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


def visit_my_courses(user):
    update_client(user.client)
    logging.info("[TASK] visit my courses")
    student.visit_my_courses()


def visit_one_course(user):
    update_client(user.client)
    logging.info("[TASK] visit one course")
    student.visit_one_course()


def start_one_course(user):
    update_client(user.client)
    logging.info("[TASK] start one course")
    student.start_one_course()


def download_one_attachment_from_one_course(user):
    update_client(user.client)
    logging.info("[TASK] download one attachment from one course")
    student.download_one_attachment_from_one_course()


def update_client(client):
    student.identity_api_endpoint.client = client
    student.users_api.client = client
    student.lms_users_api.client = client
    student.objectives_api.client = client
    student.objective_workflow_aggregates_api.client = client
    student.activity_records_api.client = client
    student.start_objective_workflows_api.client = client
    student.start_activity_workflows_api.client = client
    student.finish_activity_workflows_api.client = client
