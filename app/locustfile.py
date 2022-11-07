from locust import HttpUser, task, between, LoadTestShape
from app.profiles.admin import Admin
from app.profiles.instructor import Instructor
from app.profiles.student import Student
from app.drivers.database_driver import db_driver
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.mail_messages_api import MailMessagesAPI
from app.apis.account_reset_password_api import AccountResetPasswordAPI
from app.apis.roles_api import RolesAPI
from app.apis.user_roles_api import UserRolesAPI
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

# deprecated
# class AdminUser(HttpUser):
#     weight = 1
#     wait_time = between(6, 10)
#     task_weights = [1, 5, 40]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         identity_api_endpoint = IdentityAPIEndPoint(client=self.client)
#         lms_users_api = LmsUsersAPI(db_driver, client=self.client)
#         mail_messages_api = MailMessagesAPI(client=self.client)
#         account_reset_password_api = AccountResetPasswordAPI(db_driver, self.client)
#         roles_api = RolesAPI(client=self.client)
#         user_roles_api = UserRolesAPI(client=self.client)
#         self.admin = Admin(
#             db_driver,
#             identity_api_endpoint,
#             lms_users_api,
#             mail_messages_api,
#             account_reset_password_api,
#             roles_api,
#             user_roles_api,
#         )
#         # use specific url for each request
#         self.client.base_url = ""

#     @task(task_weights[2])
#     def create_admin_user(self):
#         self.admin.create_admin_user()

#     @task(task_weights[3])
#     def create_instructor_user(self):
#         self.admin.create_instructor_user()

#     @task(task_weights[4])
#     def create_student_user(self):
#         self.admin.create_student_user()


class InstructorUser(HttpUser):
    WEIGHT_BEFORE_ENROLL = 10
    WEIGHT_AFTER_ENROLL = 1
    TASK_WEIGHTS_BEFORE_ENROLL = [100, 5, 20, 10, 10]
    TASK_WEIGHTS_AFTER_ENROLL = [1, 1, 100, 30, 30]
    weight = 1
    wait_time = between(6, 10)
    task_weights = [1, 1, 1, 1, 1]

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
        logging.info("enroll one student")
        self.instructor.enroll_one_student()

    @task(task_weights[1])
    def expel_one_student(self):
        logging.info("expel one student")
        self.instructor.expel_one_student()

    @task(task_weights[2])
    def edit_one_course_description(self):
        logging.info("edit one course description")
        self.instructor.edit_one_course_description()

    @task(task_weights[3])
    def upload_one_image_to_course(self):
        logging.info("upload one image to course")
        self.instructor.upload_one_image_to_course()

    @task(task_weights[4])
    def upload_one_attachment_to_course(self):
        logging.info("upload one attachment to course")
        self.instructor.upload_one_attachment_to_course()


class StudentUser(HttpUser):
    WEIGHT_BEFORE_ENROLL = 1
    WEIGHT_AFTER_ENROLL = 10
    TASK_WEIGHTS_BEFORE_ENROLL = [100, 1]
    TASK_WEIGHTS_AFTER_ENROLL = [1, 2]
    weight = 1
    wait_time = between(6, 10)
    # according to visited times of icorsi pages /course and /my
    task_weights = [1, 1]

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
        logging.info("visit my courses")
        self.student.visit_my_courses()

    @task(task_weights[1])
    def take_course(self):
        logging.info("take course")
        self.student.take_course()


class StagesShape(LoadTestShape):
    PERIOD_DURATION = 60
    ENROLL_DDL = PERIOD_DURATION * 10

    def __init__(self, time_intervals: int = PERIOD_DURATION):
        self.enroll_ddl_remind = False
        df = pd.read_csv("./app/workload.csv")
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
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                if run_time < self.ENROLL_DDL:
                    InstructorUser.weight = InstructorUser.WEIGHT_BEFORE_ENROLL
                    InstructorUser.task_weights = (
                        InstructorUser.TASK_WEIGHTS_BEFORE_ENROLL
                    )
                    StudentUser.weight = StudentUser.WEIGHT_BEFORE_ENROLL
                    StudentUser.task_weights = StudentUser.TASK_WEIGHTS_BEFORE_ENROLL
                else:
                    if not self.enroll_ddl_remind:
                        logging.info("enrollment reaches deadline")
                    InstructorUser.weight = InstructorUser.WEIGHT_AFTER_ENROLL
                    InstructorUser.task_weights = (
                        InstructorUser.TASK_WEIGHTS_AFTER_ENROLL
                    )
                    StudentUser.weight = StudentUser.WEIGHT_AFTER_ENROLL
                    StudentUser.task_weights = StudentUser.TASK_WEIGHTS_AFTER_ENROLL
                tick_data = (stage["num_of_users"], stage["spawn_rate"])
                return tick_data
        return None
