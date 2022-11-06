from app.apis.users_api import UsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.objective_workflow_aggregates_api import ObjectiveWorkflowAggregatesAPI
from app.apis.activity_records_api import ActivityRecordsAPI
from app.apis.start_objective_workflows_api import StartObjectiveWorkflowsAPI
from app.apis.start_activity_workflows_api import StartActivityWorkflowsAPI
import random
from app.models.user import User


class Student:
    """A class to represent the profile of students."""

    def __init__(
        self,
        users_api: UsersAPI,
        objectives_api: ObjectivesAPI,
        objective_workflow_aggregates_api: ObjectiveWorkflowAggregatesAPI,
        activity_records_api: ActivityRecordsAPI,
        start_objective_workflows_api: StartObjectiveWorkflowsAPI,
        start_activity_workflows_api: StartActivityWorkflowsAPI,
    ):
        self.users_api = users_api
        self.objectives_api = objectives_api
        self.objective_workflow_aggregates_api = objective_workflow_aggregates_api
        self.activity_records_api = activity_records_api
        self.start_objective_workflows_api = start_objective_workflows_api
        self.start_activity_workflows_api = start_activity_workflows_api

    def login(self, user: User) -> dict:
        """
        Login a student user.
        :param user: User object to login.
        :return: A HTTP header with authorization token.
        """
        pass

    def take_course(self, user: User, headers: dict):
        course = self.select_one_course()
        if course is not None:
            self.objectives_api.get_objective_workflow_aggregate_by_id(
                course["objective"]["id"]
            )
            objective = self.objectives_api.get_objective_by_id(
                course["objective"]["id"]
            )
            self.objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
                course["id"]
            )
            self.objective_workflow_aggregates_api.get_objective_records_by_id(
                course["id"]
            )
            if course["lastObjectiveWorkflow"] is None:
                self.activity_records_api.get_activity_records_by_query(
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=",{objective.activity.id}],"and",["userId","=",{user.id}]]',
                    }
                )
                # when press start button
                objective_workflow_id = (
                    self.start_objective_workflows_api.start_objective_workflow(
                        headers, course["id"]
                    )
                )
                self.objective_workflow_aggregates_api.get_objective_records_by_id(
                    course["id"]
                )
                self.users_api.get_user_activity_workflow_aggregates_by_query(
                    headers,
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=",{objective.activity.id}],"and",["userId","=",{user.id}]]',
                    },
                )
                self.start_activity_workflows_api.start_activity_workflow(
                    headers, objective_workflow_id
                )
                self.objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
                    course["id"]
                )
                self.users_api.get_user_activity_workflow_aggregates_by_query(
                    headers,
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=",{objective.activity.id}],"and",["userId","=",{user.id}]]',
                    },
                )
                self.objective_workflow_aggregates_api.get_activity_with_aggregates_by_id(
                    headers, course["id"], objective.activity.id
                )
                objective = self.objectives_api.get_objective_by_id(
                    course["objective"]["id"]
                )
            else:
                self.users_api.get_user_activity_workflow_aggregates_by_query(
                    headers,
                    {
                        "requireTotalCount": True,
                        "filter": f'[["activity.id","=",{objective.activity.id}],"and",["userId","=",{user.id}]]',
                    },
                )
                # when press continue button
                self.objective_workflow_aggregates_api.get_activity_with_aggregates_by_id(
                    headers, course["id"], objective.activity.id
                )

    def select_one_course(self) -> dict | None:
        courses = self.users_api.get_user_objective_workflow_aggregates()
        if len(courses) > 0:
            return random.choice(courses)
        else:
            return None
