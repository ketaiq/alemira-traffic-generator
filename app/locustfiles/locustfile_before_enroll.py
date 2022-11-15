from locust import LoadTestShape
import pandas as pd
import logging
from locust import HttpUser, task, between
from app.profiles.instructor import Instructor
from app.profiles.student import Student
from app.drivers.database_driver import db_driver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.users_api import UsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.personal_enrollments_api import PersonalEnrollmentsAPI
from app.apis.objective_workflow_aggregates_api import ObjectiveWorkflowAggregatesAPI
from app.apis.activity_records_api import ActivityRecordsAPI
from app.apis.start_objective_workflows_api import StartObjectiveWorkflowsAPI
from app.apis.start_activity_workflows_api import StartActivityWorkflowsAPI
import pandas as pd
import logging


class InstructorUser(HttpUser):
    weight = 2
    wait_time = between(6, 10)
    task_weights = [100, 5, 20, 10, 10]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        identity_api_endpoint = IdentityAPIEndPoint(client=self.client)
        users_api = UsersAPI(client=self.client)
        lms_users_api = LmsUsersAPI(db_driver, client=self.client)
        objectives_api = ObjectivesAPI(db_driver, client=self.client)
        personal_enrollments_api = PersonalEnrollmentsAPI(db_driver, client=self.client)
        self.instructor = Instructor(
            db_driver,
            identity_api_endpoint,
            users_api,
            lms_users_api,
            objectives_api,
            personal_enrollments_api,
        )
        # use specific url for each request
        self.client.base_url = ""

    @task(task_weights[0])
    def enroll_one_student(self):
        logging.info("[TASK] enroll one student")
        self.instructor.enroll_one_student()

    @task(task_weights[1])
    def expel_one_student(self):
        logging.info("[TASK] expel one student")
        self.instructor.expel_one_student()

    @task(task_weights[2])
    def edit_one_course_description(self):
        logging.info("[TASK] edit one course description")
        self.instructor.edit_one_course_description()

    @task(task_weights[3])
    def upload_one_image_to_course(self):
        logging.info("[TASK] upload one image to course")
        self.instructor.upload_one_image_to_course_description()

    @task(task_weights[4])
    def upload_one_attachment_to_course(self):
        logging.info("[TASK] upload one attachment to course")
        self.instructor.upload_one_attachment_to_course_description()


class StudentUser(HttpUser):
    weight = 1
    wait_time = between(6, 10)
    # according to visited times of icorsi pages /course and /my
    task_weights = [100, 1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        identity_api_endpoint = IdentityAPIEndPoint(client=self.client)
        users_api = UsersAPI(client=self.client)
        lms_users_api = LmsUsersAPI(db_driver, client=self.client)
        objectives_api = ObjectivesAPI(db_driver, client=self.client)
        objective_workflow_aggregates_api = ObjectiveWorkflowAggregatesAPI(
            client=self.client
        )
        activity_records_api = ActivityRecordsAPI(client=self.client)
        start_objective_workflows_api = StartObjectiveWorkflowsAPI(client=self.client)
        start_activity_workflows_api = StartActivityWorkflowsAPI(client=self.client)
        self.student = Student(
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
        # use specific url for each request
        self.client.base_url = ""

    @task(task_weights[0])
    def visit_my_courses(self):
        logging.info("[TASK] visit my courses")
        self.student.visit_my_courses()

    @task(task_weights[1])
    def visit_a_specific_course(self):
        logging.info("[TASK] take course")
        self.student.visit_one_course()


class ShapeBeforeEnroll(LoadTestShape):
    PERIOD_DURATION = 60
    ENROLL_DDL = PERIOD_DURATION
    WORKLOAD_FILE = "app/workload/workload_before_enroll.csv"

    def __init__(self, time_intervals: int = PERIOD_DURATION):
        self.enroll_ddl_remind = False
        df = pd.read_csv(self.WORKLOAD_FILE)
        self.stages = []
        duration = time_intervals
        for index in df.index:
            self.stages.append(
                {
                    "duration": duration,
                    "num_of_users": df.loc[index, "Users"],
                    "spawn_rate": df.loc[index, "SpawnRate"],
                }
            )
            duration += time_intervals

    def tick(self):
        if not self.enroll_ddl_remind:
            logging.info("enrollment begins")
            self.enroll_ddl_remind = True
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["num_of_users"], stage["spawn_rate"])
                return tick_data
        return None
