from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.personal_enrollments_api import PersonalEnrollmentsAPI
import random, logging, os
from app.models.user import User
from app.models.objective.objective import Objective
from app.exceptions import (
    UserNotFoundException,
    ObjectiveNotFoundException,
    ObjectivePersonalEnrollmentNotFoundException,
)
from app.drivers.database_driver import DatabaseDriver
from app.models.personal_enrollment import PersonalEnrollment
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.models.role import Role


class Instructor:
    """A class to represent the profile of instructors."""

    def __init__(
        self,
        db_driver: DatabaseDriver,
        identity_api_endpoint: IdentityAPIEndPoint,
        users_api: UsersAPI,
        lms_users_api: LmsUsersAPI,
        objectives_api: ObjectivesAPI,
        personal_enrollments_api: PersonalEnrollmentsAPI,
    ):
        self.db_driver = db_driver
        self.identity_api_endpoint = identity_api_endpoint
        self.users_api = users_api
        self.lms_users_api = lms_users_api
        self.objectives_api = objectives_api
        self.personal_enrollments_api = personal_enrollments_api

    def enroll_one_student(self):
        headers = self._get_instructor_headers()
        objective_to_enroll = self.select_one_objective(headers)
        self._enroll_one_student(headers, objective_to_enroll)

    def expel_one_student(self):
        headers = self._get_instructor_headers()
        objective_to_expel = self.select_one_objective(headers)
        self._expel_one_student(headers, objective_to_expel)

    def edit_one_course_description(self):
        headers = self._get_instructor_headers()
        objective_to_edit = self.select_one_objective(headers)
        self._edit_one_course_description(headers, objective_to_edit)

    def upload_one_image_to_course(self):
        headers = self._get_instructor_headers()
        objective_to_upload_one_image = self.select_one_objective(headers)
        self._upload_one_image_to_course(headers, objective_to_upload_one_image)

    def upload_one_attachment_to_course(self):
        headers = self._get_instructor_headers()
        objective_to_upload_one_attachment = self.select_one_objective(headers)
        self._upload_one_attachment_to_course(
            headers, objective_to_upload_one_attachment
        )

    def _edit_one_course_description(self, headers: dict, objective: Objective):
        objective = objective.gen_random_update()
        self.objectives_api.update_objective(headers, objective)

    def _upload_one_image_to_course(self, headers: dict, objective: Objective):
        image_filename = self.select_one_image()
        self.objectives_api.upload_image_to_objective(
            headers, objective, image_filename
        )

    def _upload_one_attachment_to_course(self, headers: dict, objective: Objective):
        attachment_filename = self.select_one_attachment()
        self.objectives_api.upload_attachment_to_objective(
            headers, objective, attachment_filename
        )

    def _enroll_one_student(self, headers: dict, objective: Objective):
        # enroll the student in the course
        user_to_enroll = self.select_one_student(headers)
        self.personal_enrollments_api.create_personal_enrollment(
            headers, objective.id, user_to_enroll.id
        )

    def _expel_one_student(self, headers: dict, objective: Objective):
        # get all personal enrollments in this course objective
        skip = 0
        take = 10
        try:
            res = self.objectives_api.get_objective_personal_enrollments_by_query(
                headers,
                objective.id,
                {
                    "skip": skip,
                    "take": take,
                    "requireTotalCount": True,
                },
            )
            if not res["data"]:
                raise ObjectivePersonalEnrollmentNotFoundException(
                    f"No personal enrollment in objective {objective.id}"
                )
            personal_enrollment_dict = random.choice(res["data"])
            self.personal_enrollments_api.delete_personal_enrollment_by_id(
                headers, personal_enrollment_dict["id"]
            )
        except ObjectivePersonalEnrollmentNotFoundException as e:
            logging.error(e.message)

    def select_one_student(self, headers: dict) -> User:
        # select a random student from mongodb
        # check student exists, otherwise select again
        user = None
        while user is None:
            user = self._select_one_student(headers)
        return user

    def _select_one_student(self, headers: dict) -> User:
        username = random.choice(self.db_driver.find_student_usernames())
        res = self.users_api.get_users_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["username","=","{username}"]',
            },
        )
        try:
            if res["totalCount"] > 0:
                user = User(res["data"][0])
                self.db_driver.update_user(user)
                return user
            else:
                raise UserNotFoundException(f"Username {username} doesn't exist.")
        except UserNotFoundException as e:
            logging.error(e.message)

    def select_one_objective(self, headers: dict) -> Objective:
        # select a random course objective
        objective = None
        while objective is None:
            objective = self._select_one_objective(headers)
        return objective

    def _select_one_objective(self, headers: dict) -> Objective:
        course_code = random.choice(self.db_driver.find_courses_codes())
        res = self.objectives_api.get_objectives_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["code","=","{course_code}"]',
            },
        )
        try:
            if res["totalCount"] > 0:
                objective = Objective(res["data"][0])
                self.db_driver.update_objective(objective)
                return objective
            else:
                raise ObjectiveNotFoundException(
                    f"Objective code {course_code} doesn't exist."
                )
        except ObjectiveNotFoundException as e:
            logging.error(e.message)

    def select_one_image(self) -> str:
        return random.choice(os.listdir("resources/images"))

    def select_one_attachment(self) -> str:
        return random.choice(os.listdir("resources/attachments"))

    def _get_instructor_headers(self) -> dict:
        return self.identity_api_endpoint.get_headers(
            Role.INSTRUCTOR, self._select_one_instructor()
        )

    def _select_one_instructor(self) -> User:
        return User(random.choice(self.db_driver.find_instructor_users()))
