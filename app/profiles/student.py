from app.drivers.database_driver import DatabaseDriver
from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.objective_workflow_aggregates_api import ObjectiveWorkflowAggregatesAPI
from app.apis.activity_records_api import ActivityRecordsAPI
from app.apis.start_objective_workflows_api import StartObjectiveWorkflowsAPI
from app.apis.start_activity_workflows_api import StartActivityWorkflowsAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
import random
from app.models.user import User
from app.models.role import Role


class Student:
    """A class to represent the profile of students."""

    def __init__(
        self,
        db_driver: DatabaseDriver,
        identity_api_endpoint: IdentityAPIEndPoint,
        users_api: UsersAPI,
        lms_users_api: LmsUsersAPI,
        objectives_api: ObjectivesAPI,
        objective_workflow_aggregates_api: ObjectiveWorkflowAggregatesAPI,
        activity_records_api: ActivityRecordsAPI,
        start_objective_workflows_api: StartObjectiveWorkflowsAPI,
        start_activity_workflows_api: StartActivityWorkflowsAPI,
    ):
        self.db_driver = db_driver
        self.identity_api_endpoint = identity_api_endpoint
        self.users_api = users_api
        self.lms_users_api = lms_users_api
        self.objectives_api = objectives_api
        self.objective_workflow_aggregates_api = objective_workflow_aggregates_api
        self.activity_records_api = activity_records_api
        self.start_objective_workflows_api = start_objective_workflows_api
        self.start_activity_workflows_api = start_activity_workflows_api

    def take_course(self):
        headers = self._get_student_headers()
        me = self.lms_users_api.get_user_me(headers)
        self._take_course(headers, me)

    def _take_course(self, headers: dict, user: User) -> str | None:
        """
        Perform a student's actions of taking a course.
        :return: Course objective workflow aggregate id.
        """
        course = self.select_one_course(headers, user.id)
        if course is not None:
            self.objectives_api.get_objective_workflow_aggregate_by_id(
                headers, course["objective"]["id"]
            )
            objective = self.objectives_api.get_objective_by_id(
                headers, course["objective"]["id"]
            )
            self.objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
                headers, course["id"]
            )
            self.objective_workflow_aggregates_api.get_objective_records_by_id(
                headers, course["id"]
            )
            if course["lastObjectiveWorkflow"] is None:
                self.activity_records_api.get_activity_records_by_query(
                    headers,
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=","{objective.activity.id}"],"and",["user.id","=","{user.id}"]]',
                    },
                )
                # when press start button
                objective_workflow_id = (
                    self.start_objective_workflows_api.start_objective_workflow(
                        headers, course["id"]
                    )
                )
                self.objective_workflow_aggregates_api.get_objective_records_by_id(
                    headers, course["id"]
                )
                self.users_api.get_user_activity_workflow_aggregates_by_query(
                    headers,
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=","{objective.activity.id}"],"and",["userId","=","{user.id}"]]',
                    },
                )
                self.start_activity_workflows_api.start_activity_workflow(
                    headers, objective_workflow_id
                )
                self.objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
                    headers, course["id"]
                )
                self.users_api.get_user_activity_workflow_aggregates_by_query(
                    headers,
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=","{objective.activity.id}"],"and",["userId","=","{user.id}"]]',
                    },
                )
                self.objective_workflow_aggregates_api.get_activity_with_aggregates_by_id(
                    headers, course["id"], objective.activity.id
                )
                objective = self.objectives_api.get_objective_by_id(
                    headers, course["objective"]["id"]
                )
            else:
                self.users_api.get_user_activity_workflow_aggregates_by_query(
                    headers,
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=","{objective.activity.id}"],"and",["userId","=","{user.id}"]]',
                    },
                )
                # when press continue button
                self.objective_workflow_aggregates_api.get_activity_with_aggregates_by_id(
                    headers, course["id"], objective.activity.id
                )
            return course["id"]

    def select_one_course(self, headers: dict, user_id: str) -> dict | None:
        courses = self.users_api.get_user_objective_workflow_aggregates(
            headers, user_id
        )
        if len(courses) > 0:
            return random.choice(courses)
        else:
            return None

    def _get_student_headers(self) -> dict:
        """
        Login a student user.
        :return: A HTTP header with authorization token.
        """
        return self.identity_api_endpoint.get_headers(
            Role.STUDENT, self._select_one_student()
        )

    def _select_one_student(self) -> User:
        return User(random.choice(self.db_driver.find_student_users()))
