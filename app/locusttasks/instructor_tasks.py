import logging
from app.drivers.database_driver import db_driver
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.personal_enrollments_api import PersonalEnrollmentsAPI
from app.apis.activities_api import ActivitiesAPI
from app.profiles.instructor import Instructor

identity_api_endpoint = IdentityAPIEndPoint()
users_api = UsersAPI()
lms_users_api = LmsUsersAPI(db_driver)
objectives_api = ObjectivesAPI(db_driver)
personal_enrollments_api = PersonalEnrollmentsAPI(db_driver)
activities_api = ActivitiesAPI(db_driver)
instructor = Instructor(
    db_driver,
    identity_api_endpoint,
    users_api,
    lms_users_api,
    objectives_api,
    personal_enrollments_api,
    activities_api,
)


def enroll_one_student(user):
    update_client(user.client)
    logging.info("[TASK] enroll one student")
    instructor.enroll_one_student()


def expel_one_student(user):
    update_client(user.client)
    logging.info("[TASK] expel one student")
    instructor.expel_one_student()


def edit_one_course_description(user):
    update_client(user.client)
    logging.info("[TASK] edit one course description")
    instructor.edit_one_course_description()


def upload_one_image_to_course_description(user):
    update_client(user.client)
    logging.info("[TASK] upload one image to course description")
    instructor.upload_one_image_to_course_description()


def upload_one_attachment_to_course_description(user):
    update_client(user.client)
    logging.info("[TASK] upload one attachment to course description")
    instructor.upload_one_attachment_to_course_description()


def edit_one_course_content(user):
    update_client(user.client)
    logging.info("[TASK] edit one course content")
    instructor.edit_one_course_content()


def upload_one_image_to_course_content(user):
    update_client(user.client)
    logging.info("[TASK] upload one image to course content")
    instructor.upload_one_image_to_course_content()


def upload_one_attachment_to_course_content(user):
    update_client(user.client)
    logging.info("[TASK] upload one attachment to course content")
    instructor.upload_one_attachment_to_course_content()


def update_client(client):
    instructor.identity_api_endpoint.client = client
    instructor.users_api.client = client
    instructor.lms_users_api.client = client
    instructor.objectives_api.client = client
    instructor.personal_enrollments_api.client = client
    instructor.activities_api.client = client
