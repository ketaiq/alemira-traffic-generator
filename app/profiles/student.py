from app.drivers.database_driver import DatabaseDriver
from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.objective_workflow_aggregates_api import ObjectiveWorkflowAggregatesAPI
from app.apis.activity_records_api import ActivityRecordsAPI
from app.apis.start_objective_workflows_api import StartObjectiveWorkflowsAPI
from app.apis.start_activity_workflows_api import StartActivityWorkflowsAPI
from app.apis.finish_activity_workflows_api import FinishActivityWorkflow
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
import random, logging
from app.models.user import User
from app.models.role import Role
from app.models.objective.objective import Objective


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
        finish_activity_workflows_api: FinishActivityWorkflow,
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
        self.finish_activity_workflows_api = finish_activity_workflows_api

    def visit_my_courses(self):
        headers = self._get_student_headers()
        me = self.lms_users_api.get_user_me(headers)
        logging.info(f"student {me.username} visits my courses.")
        self.users_api.get_user_permissions(headers)
        self.users_api.get_user_roles(headers)
        self.users_api.get_user_objective_workflow_aggregates(headers, me.id)

    def visit_one_course(self):
        headers = self._get_student_headers()
        me = self.lms_users_api.get_user_me(headers)
        self._visit_one_course(headers, me)

    def start_one_course(self):
        headers = self._get_student_headers()
        me = self.lms_users_api.get_user_me(headers)
        self._start_one_course(headers, me)

    def finish_one_course(self):
        headers = self._get_student_headers()
        me = self.lms_users_api.get_user_me(headers)
        self._finish_one_course(headers, me)

    def review_one_course(self):
        headers = self._get_student_headers()
        me = self.lms_users_api.get_user_me(headers)
        self._review_one_course(headers, me)

    def _visit_one_course(self, headers: dict, user: User):
        """
        Perform a student's actions of taking a course.
        :return: Course objective workflow aggregate id.
        """
        course = self._select_one_course(headers, user.id)
        if course is None:
            logging.warning(f"student {user.username} doesn't take any courses!")
            return
        course_code = course["objective"]["code"]
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
        if course["lastObjectiveWorkflow"]:
            # Visit a course if the chosen course has been started
            self._visit_course(headers, course, objective, user)
            logging.info(f"student {user.username} visits course {course_code}.")
        # Download an attachment from a course (70% probability if exists)
        objective = self.objectives_api.get_objective_by_id(
            headers, course["objective"]["id"]
        )
        if objective.has_attachment() and random.choices([True, False], (40, 60), k=1):
            self.objectives_api.download_attachment_from_objective(
                objective.get_attachment_url()
            )
            logging.info(
                f"student {user.username} downloads attachment from course {course_code}."
            )

    def _select_one_course(self, headers: dict, user_id: str) -> dict | None:
        courses = self.users_api.get_user_objective_workflow_aggregates(
            headers, user_id
        )
        if len(courses) > 0:
            return random.choice(courses)
        else:
            return None

    def _select_one_course_to_start(self, headers: dict, user_id: str) -> dict | None:
        courses = self.users_api.get_user_objective_workflow_aggregates(
            headers, user_id
        )
        courses_to_start = []
        for course in courses:
            if course["lastObjectiveWorkflow"] is None:
                courses_to_start.append(course)
        if len(courses_to_start) > 0:
            return random.choice(courses_to_start)
        else:
            return None

    def _select_one_course_to_finish(self, headers: dict, user_id: str) -> dict | None:
        courses = self.users_api.get_user_objective_workflow_aggregates(
            headers, user_id
        )
        courses_to_finish = []
        for course in courses:
            if (
                course["lastObjectiveWorkflow"]
                and course["lastObjectiveWorkflow"]["created"]
                and not course["lastObjectiveWorkflow"]["finished"]
            ):
                courses_to_finish.append(course)
        if len(courses_to_finish) > 0:
            return random.choice(courses_to_finish)
        else:
            return None

    def _select_one_course_to_review(self, headers: dict, user_id: str) -> dict | None:
        courses = self.users_api.get_user_objective_workflow_aggregates(
            headers, user_id
        )
        courses_to_review = []
        for course in courses:
            if (
                course["lastObjectiveWorkflow"]
                and course["lastObjectiveWorkflow"]["created"]
                and course["lastObjectiveWorkflow"]["finished"]
            ):
                courses_to_review.append(course)
        if len(courses_to_review) > 0:
            return random.choice(courses_to_review)
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

    def _start_one_course(self, headers: dict, user: User):
        # select a course that can be started
        course = self._select_one_course_to_start(headers, user.id)
        if course is None:
            logging.warning(
                f"student {user.username} doesn't have any courses that can be started!"
            )
            return
        objective_id = course["objective"]["id"]
        objective = self.objectives_api.get_objective_by_id(headers, objective_id)
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
        logging.info(f"student {user.username} starts course {objective.code}.")

    def _visit_course(
        self, headers: dict, course: dict, objective: Objective, user: User
    ):
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

    def _finish_one_course(self, headers: dict, user: User):
        # select a course that can be finished
        course = self._select_one_course_to_finish(headers, user.id)
        if course is None:
            logging.warning(
                f"student {user.username} doesn't have any courses that can be finished!"
            )
            return

        objective_id = course["objective"]["id"]
        objective_workflow_aggregate_id = course["id"]
        objective_workflow_aggregate = self.objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
            headers, objective_workflow_aggregate_id
        )
        objective_workflow_id = objective_workflow_aggregate["lastObjectiveWorkflow"][
            "id"
        ]
        objective = self.objectives_api.get_objective_by_id(headers, objective_id)
        activity_id = objective.activity.id
        activity_with_aggregates = (
            self.objective_workflow_aggregates_api.get_activity_with_aggregates_by_id(
                headers, objective_workflow_aggregate_id, activity_id
            )
        )
        activity_workflow_ids = [
            activity_with_aggregates["activityWorkflowAggregate"][
                "lastActivityWorkflow"
            ]["id"]
        ]
        # post finish-activity-workflows
        self.finish_activity_workflows_api.create_finish_activity_workflow(
            headers, activity_workflow_ids, objective_workflow_id
        )
        logging.info(f"student {user.username} finishes course {objective.code}.")

    def _review_one_course(self, headers: dict, user: User):
        # select a course that can be reviewed
        course = self._select_one_course_to_review(headers, user.id)
        if course is None:
            logging.warning(
                f"student {user.username} doesn't have any finished courses that can be reviewed!"
            )
            return
        objective_id = course["objective"]["id"]
        objective_workflow_aggregate_id = course["id"]
        self.objective_workflow_aggregates_api.get_objective_workflow_aggregate_by_id(
            headers, objective_workflow_aggregate_id
        )
        self.objective_workflow_aggregates_api.get_objective_records_by_id(
            headers, objective_workflow_aggregate_id
        )
        objective = self.objectives_api.get_objective_by_id(headers, objective_id)
        activity_id = objective.activity.id
        self.activity_records_api.get_activity_records_by_query(
            headers,
            {
                f'[["activity.id","=","{activity_id}"],"and",["user.id","=","{user.id}"]]'
            },
        )
        self.users_api.get_user_activity_workflow_aggregates_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'[["activity.id","=","{activity_id}"],"and",["userId","=","{user.id}"]]',
            },
        )
        self.objective_workflow_aggregates_api.get_activity_with_aggregates_by_id(
            headers, objective_workflow_aggregate_id, activity_id
        )
        logging.info(f"student {user.username} reviews course {objective.code}.")
