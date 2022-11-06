from locust import HttpUser, task, between
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


class AdminUser(HttpUser):
    weight = 1
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        identity_api_endpoint = IdentityAPIEndPoint(client=self.client)
        lms_users_api = LmsUsersAPI(db_driver, client=self.client)
        mail_messages_api = MailMessagesAPI(client=self.client)
        account_reset_password_api = AccountResetPasswordAPI(db_driver, self.client)
        roles_api = RolesAPI(client=self.client)
        user_roles_api = UserRolesAPI(client=self.client)
        self.admin = Admin(
            db_driver,
            identity_api_endpoint,
            lms_users_api,
            mail_messages_api,
            account_reset_password_api,
            roles_api,
            user_roles_api,
        )
        # use specific url for each request
        self.client.base_url = ""

    @task(100)
    def get_num_of_users(self):
        self.admin.get_num_of_users()

    @task(1)
    # TODO use dynamic weight
    def create_admin_user(self):
        self.admin.create_admin_user()

    @task(5)
    # TODO use dynamic weight
    def create_instructor_user(self):
        self.admin.create_instructor_user()

    @task(40)
    # TODO use dynamic weight
    def create_student_user(self):
        self.admin.create_student_user()


class InstructorUser(HttpUser):
    weight = 5
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        identity_api_endpoint = IdentityAPIEndPoint(client=self.client)
        users_api = UsersAPI(client=self.client)
        lms_users_api = LmsUsersAPI(db_driver, client=self.client)
        objectives_api = ObjectivesAPI(db_driver, client=self.client)
        personal_enrollments_api = PersonalEnrollmentsAPI(db_driver)
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

    @task(10)
    def enroll_one_student(self):
        self.instructor.enroll_one_student()

    @task(1)
    def expel_one_student(self):
        self.instructor.expel_one_student()

    @task(20)
    def edit_one_course_description(self):
        self.instructor.edit_one_course_description()

    @task(5)
    def upload_one_image_to_course(self):
        self.instructor.upload_one_image_to_course()

    @task(5)
    def upload_one_attachment_to_course(self):
        self.instructor.upload_one_attachment_to_course()


class StudentUser(HttpUser):
    weight = 40
    wait_time = between(1, 5)

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

    @task(100)
    def take_course(self):
        self.student.take_course()
