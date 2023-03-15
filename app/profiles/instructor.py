from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.activities_api import ActivitiesAPI
from app.apis.personal_enrollments_api import PersonalEnrollmentsAPI
import random, logging, os
from app.models.user import User
from app.models.objective.objective import Objective
from app.models.activity.activity import Activity
from app.exceptions.required_object_not_found import (
    UserNotFoundException,
    ObjectiveNotFoundException,
    ObjectivePersonalEnrollmentNotFoundException,
    ActivityNotFoundException,
)
from app.drivers.database_driver import DatabaseDriver
from app.models.personal_enrollment import PersonalEnrollment
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.models.role import Role
from app.utils.time import sleep_for_seconds


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
        activities_api: ActivitiesAPI,
    ):
        self.db_driver = db_driver
        self.identity_api_endpoint = identity_api_endpoint
        self.users_api = users_api
        self.lms_users_api = lms_users_api
        self.objectives_api = objectives_api
        self.personal_enrollments_api = personal_enrollments_api
        self.activities_api = activities_api

    def enroll_one_student(self):
        headers = self._get_instructor_headers()
        try:
            objective_to_enroll = self._select_one_objective(headers)
            self._enroll_one_student(headers, objective_to_enroll)
        except ObjectiveNotFoundException as e:
            logging.error(e.message)

    def expel_one_student(self):
        headers = self._get_instructor_headers()
        try:
            objective_to_expel = self._select_one_objective(headers)
            self._expel_one_student(headers, objective_to_expel)
        except ObjectiveNotFoundException as e:
            logging.error(e.message)
        except ObjectivePersonalEnrollmentNotFoundException as e:
            logging.warning(e.message)

    def edit_one_course_description(self):
        # update an objective
        headers = self._get_instructor_headers()
        try:
            objective_to_edit = self._select_one_objective(headers)
            self._edit_one_course_description(headers, objective_to_edit)
        except ObjectiveNotFoundException as e:
            logging.error(e.message)

    def edit_one_course_content(self):
        # update an activity
        headers = self._get_instructor_headers()
        try:
            activity_to_edit = self._select_one_activity(headers)
            self._edit_one_course_content(headers, activity_to_edit)
        except ActivityNotFoundException as e:
            logging.error(e.message)

    def upload_one_image_to_course_description(self):
        sleep_for_seconds(60 * 2, 60 * 5)
        headers = self._get_instructor_headers()
        try:
            objective_to_upload_one_image = self._select_one_objective(headers)
            self._upload_one_image_to_course_description(
                headers, objective_to_upload_one_image
            )
        except ObjectiveNotFoundException as e:
            logging.error(e.message)

    def upload_one_attachment_to_course_description(self):
        sleep_for_seconds(60 * 2, 60 * 5)
        headers = self._get_instructor_headers()
        try:
            objective_to_upload_one_attachment = self._select_one_objective(headers)
            self._upload_one_attachment_to_course_description(
                headers, objective_to_upload_one_attachment
            )
        except ObjectiveNotFoundException as e:
            logging.error(e.message)

    def upload_one_image_to_course_content(self):
        sleep_for_seconds(60 * 2, 60 * 5)
        headers = self._get_instructor_headers()
        try:
            activity_to_upload_one_image = self._select_one_activity(headers)
            self._upload_one_image_to_course_content(
                headers, activity_to_upload_one_image
            )
        except ActivityNotFoundException as e:
            logging.error(e.message)

    def upload_one_attachment_to_course_content(self):
        sleep_for_seconds(60 * 2, 60 * 5)
        headers = self._get_instructor_headers()
        try:
            activity_to_upload_one_attachment = self._select_one_activity(headers)
            self._upload_one_attachment_to_course_content(
                headers, activity_to_upload_one_attachment
            )
        except ActivityNotFoundException as e:
            logging.error(e.message)

    def _edit_one_course_description(self, headers: dict, objective: Objective):
        objective = objective.gen_random_update()
        self.objectives_api.update_objective(headers, objective)

    def _edit_one_course_content(self, headers: dict, activity: Activity):
        activity = activity.gen_random_update()
        self.activities_api.update_activity(headers, activity)

    def _upload_one_image_to_course_description(
        self, headers: dict, objective: Objective
    ):
        image_filename = self.select_one_image()
        logging.info(
            f"upload image {image_filename} to description of course {objective.code}."
        )
        self.objectives_api.upload_image_to_objective(
            headers, objective, image_filename
        )

    def _upload_one_attachment_to_course_description(
        self, headers: dict, objective: Objective
    ):
        attachment_filename = self.select_one_attachment()
        logging.info(
            f"upload attachment {attachment_filename} to description of course {objective.code}."
        )
        self.objectives_api.upload_attachment_to_objective(
            headers, objective, attachment_filename
        )

    def _upload_one_image_to_course_content(self, headers: dict, activity: Activity):
        image_filename = self.select_one_image()
        logging.info(
            f"upload image {image_filename} to content of course {activity.code}."
        )
        self.activities_api.upload_image_to_activity(headers, activity, image_filename)

    def _upload_one_attachment_to_course_content(
        self, headers: dict, activity: Activity
    ):
        attachment_filename = self.select_one_attachment()
        logging.info(
            f"upload attachment {attachment_filename} to content of course {activity.code}."
        )
        self.activities_api.upload_attachment_to_activity(
            headers, activity, attachment_filename
        )

    def _enroll_one_student(self, headers: dict, objective: Objective):
        # enroll the student in the course
        try:
            user_to_enroll = self._select_one_student(headers)
            logging.info(
                f"enroll student {user_to_enroll.username} to course {objective.code}."
            )
            self.personal_enrollments_api.create_personal_enrollment(
                headers, objective.id, user_to_enroll.id
            )
        except UserNotFoundException as e:
            logging.error(e.message)

    def _expel_one_student(self, headers: dict, objective: Objective):
        # get all personal enrollments in this course objective
        skip = 0
        take = 10
        res = self.objectives_api.get_objective_personal_enrollments_by_query(
            headers,
            objective.id,
            {
                "skip": skip,
                "take": take,
                "requireTotalCount": True,
            },
        )
        if not res or res["totalCount"] == 0:
            raise ObjectivePersonalEnrollmentNotFoundException(
                f"No personal enrollment in objective {objective.id}."
            )
        personal_enrollment_dict = random.choice(res["data"])
        username = personal_enrollment_dict["user"]["username"]
        logging.info(f"expel student {username} from course {objective.code}.")
        self.personal_enrollments_api.delete_personal_enrollment_by_id(
            headers, personal_enrollment_dict["id"]
        )

    def _select_one_student(self, headers: dict) -> User:
        username = random.choice(self.db_driver.find_student_usernames())
        logging.info(f"select student {username}.")
        res = self.users_api.get_users_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["username","=","{username}"]',
            },
        )
        if res and res["totalCount"] > 0:
            user = User(res["data"][0])
            self.db_driver.update_user(user)
            return user
        else:
            raise UserNotFoundException(f"Username {username} doesn't exist.")

    def _select_one_objective(self, headers: dict) -> Objective:
        course_code = random.choice(self.db_driver.find_objective_codes())
        logging.info(f"select objective with code {course_code}.")
        res = self.objectives_api.get_objectives_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["code","=","{course_code}"]',
            },
        )
        if res and res["totalCount"] > 0:
            objective = Objective(res["data"][0])
            self.db_driver.update_objective(objective)
            return objective
        else:
            raise ObjectiveNotFoundException(
                f"Objective code {course_code} doesn't exist."
            )

    def _select_one_activity(self, headers: dict) -> Activity:
        course_code = random.choice(self.db_driver.find_activity_codes())
        logging.info(f"select activity with code {course_code}.")
        res = self.activities_api.get_activities_by_query(
            headers,
            {
                "requireTotalCount": True,
                "filter": f'["code","=","{course_code}"]',
            },
        )
        if res and res["totalCount"] > 0:
            activity = Activity(res["data"][0])
            self.db_driver.update_activity(activity)
            return activity
        else:
            raise ActivityNotFoundException(
                f"Activity code {course_code} doesn't exist."
            )

    def select_one_image(self) -> str:
        return random.choice(os.listdir("resources/images"))

    def select_one_attachment(self) -> str:
        return random.choice(os.listdir("resources/attachments"))

    def _get_instructor_headers(self) -> dict:
        return self.identity_api_endpoint.get_headers(
            Role.INSTRUCTOR, self._select_one_instructor()
        )

    def _select_one_instructor(self) -> User:
        user = User(random.choice(self.db_driver.find_instructor_users()))
        logging.info(f"select instructor {user.username}.")
        return user
