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
from app.apis.finish_activity_workflows_api import FinishActivityWorkflow
from app.apis.activities_api import ActivitiesAPI
import pandas as pd
import logging, sys


class InstructorUser(HttpUser):
    ENROLL_ONE_STUDENT_WEIGHT_FIRST = 100
    EXPEL_ONE_STUDENT_WEIGHT_FIRST = 10
    EDIT_ONE_COURSE_DESCRIPTION_WEIGHT_FIRST = 50
    UPLOAD_ONE_IMAGE_TO_COURSE_DESCRIPTION_WEIGHT_FIRST = 20
    UPLOAD_ONE_ATTACHMENT_TO_COURSE_DESCRIPTION_WEIGHT_FIRST = 20
    EDIT_ONE_COURSE_CONTENT_WEIGHT_FIRST = 20
    UPLOAD_ONE_IMAGE_TO_COURSE_CONTENT_WEIGHT_FIRST = 10
    UPLOAD_ONE_ATTACHMENT_TO_COURSE_CONTENT_WEIGHT_FIRST = 10

    ENROLL_ONE_STUDENT_WEIGHT_SECOND = 1
    EXPEL_ONE_STUDENT_WEIGHT_SECOND = 1
    EDIT_ONE_COURSE_DESCRIPTION_WEIGHT_SECOND = 20
    UPLOAD_ONE_IMAGE_TO_COURSE_DESCRIPTION_WEIGHT_SECOND = 10
    UPLOAD_ONE_ATTACHMENT_TO_COURSE_DESCRIPTION_WEIGHT_SECOND = 10
    EDIT_ONE_COURSE_CONTENT_WEIGHT_SECOND = 100
    UPLOAD_ONE_IMAGE_TO_COURSE_CONTENT_WEIGHT_SECOND = 30
    UPLOAD_ONE_ATTACHMENT_TO_COURSE_CONTENT_WEIGHT_SECOND = 30

    weight = 1
    wait_time = between(6, 10)
    task_weights = [
        ENROLL_ONE_STUDENT_WEIGHT_SECOND,
        EXPEL_ONE_STUDENT_WEIGHT_SECOND,
        EDIT_ONE_COURSE_DESCRIPTION_WEIGHT_SECOND,
        UPLOAD_ONE_IMAGE_TO_COURSE_DESCRIPTION_WEIGHT_SECOND,
        UPLOAD_ONE_ATTACHMENT_TO_COURSE_DESCRIPTION_WEIGHT_SECOND,
        EDIT_ONE_COURSE_CONTENT_WEIGHT_SECOND,
        UPLOAD_ONE_IMAGE_TO_COURSE_CONTENT_WEIGHT_SECOND,
        UPLOAD_ONE_ATTACHMENT_TO_COURSE_CONTENT_WEIGHT_SECOND,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        identity_api_endpoint = IdentityAPIEndPoint(client=self.client)
        users_api = UsersAPI(client=self.client)
        lms_users_api = LmsUsersAPI(db_driver, client=self.client)
        objectives_api = ObjectivesAPI(db_driver, client=self.client)
        personal_enrollments_api = PersonalEnrollmentsAPI(db_driver, client=self.client)
        activities_api = ActivitiesAPI(db_driver, client=self.client)
        self.instructor = Instructor(
            db_driver,
            identity_api_endpoint,
            users_api,
            lms_users_api,
            objectives_api,
            personal_enrollments_api,
            activities_api,
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
    def upload_one_image_to_course_description(self):
        logging.info("[TASK] upload one image to course description")
        self.instructor.upload_one_image_to_course_description()

    @task(task_weights[4])
    def upload_one_attachment_to_course_description(self):
        logging.info("[TASK] upload one attachment to course description")
        self.instructor.upload_one_attachment_to_course_description()

    @task(task_weights[5])
    def edit_one_course_content(self):
        logging.info("[TASK] edit one course content")
        self.instructor.edit_one_course_content()

    @task(task_weights[6])
    def upload_one_image_to_course_content(self):
        logging.info("[TASK] upload one image to course content")
        self.instructor.upload_one_image_to_course_content()

    @task(task_weights[7])
    def upload_one_attachment_to_course_content(self):
        logging.info("[TASK] upload one attachment to course content")
        self.instructor.upload_one_attachment_to_course_content()


class StudentUser(HttpUser):
    VISIT_MY_COURSES_WEIGHT_FIRST = 100
    VISIT_ONE_COURSE_WEIGHT_FIRST = 1
    START_ONE_COURSE_WEIGHT_FIRST = 1
    FINISH_ONE_COURSE_WEIGHT_FIRST = 1
    REVIEW_ONE_COURSE_WEIGHT_FIRST = 1

    VISIT_MY_COURSES_WEIGHT_SECOND = 50
    VISIT_ONE_COURSE_WEIGHT_SECOND = 100
    START_ONE_COURSE_WEIGHT_SECOND = 20
    FINISH_ONE_COURSE_WEIGHT_SECOND = 5
    REVIEW_ONE_COURSE_WEIGHT_SECOND = 5

    weight = 10
    wait_time = between(6, 10)
    # according to visited times of icorsi pages /course and /my
    task_weights = [
        VISIT_MY_COURSES_WEIGHT_SECOND,
        VISIT_ONE_COURSE_WEIGHT_SECOND,
        START_ONE_COURSE_WEIGHT_SECOND,
        FINISH_ONE_COURSE_WEIGHT_SECOND,
        REVIEW_ONE_COURSE_WEIGHT_SECOND,
    ]

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
        finish_activity_workflows_api = FinishActivityWorkflow(client=self.client)
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
            finish_activity_workflows_api,
        )
        # use specific url for each request
        self.client.base_url = ""

    @task(task_weights[0])
    def visit_my_courses(self):
        logging.info("[TASK] visit my courses")
        self.student.visit_my_courses()

    @task(task_weights[1])
    def visit_one_course(self):
        logging.info("[TASK] visit one course")
        self.student.visit_one_course()

    @task(task_weights[2])
    def start_one_course(self):
        logging.info("[TASK] start one course")
        self.student.start_one_course()

    @task(task_weights[3])
    def finish_one_course(self):
        logging.info("[TASK] finish one course")
        self.student.finish_one_course()

    @task(task_weights[4])
    def review_one_course(self):
        logging.info("[TASK] review one course")
        self.student.review_one_course()


class StagesShape(LoadTestShape):
    PERIOD_DURATION = 60
    WORKLOAD_FILE = "app/workload/workload.csv"

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
            logging.info("enrollment reaches deadline")
            self.enroll_ddl_remind = True
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["num_of_users"], stage["spawn_rate"])
                return tick_data
        sys.exit(0)
