from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.personal_enrollments_api import PersonalEnrollmentsAPI
import random, logging
from app.models.user import User
from app.models.objective.objective import Objective
from app.exceptions import (
    UserNotFoundException,
    ObjectiveNotFoundException,
    ObjectivePersonalEnrollmentNotFoundException,
)
from app.drivers.database_driver import DatabaseDriver
from app.models.personal_enrollment import PersonalEnrollment


class Instructor:
    """A class to represent the profile of instructors."""

    def __init__(
        self,
        db_driver: DatabaseDriver,
        users_api: UsersAPI,
        lms_users_api: LmsUsersAPI,
        objectives_api: ObjectivesAPI,
        personal_enrollments_api: PersonalEnrollmentsAPI,
        client=None,
    ):
        self.db_driver = db_driver
        self.users_api = users_api
        self.lms_users_api = lms_users_api
        self.objectives_api = objectives_api
        self.personal_enrollments_api = personal_enrollments_api
        self.client = client

    def enroll_one_student(self, user: User, objective: Objective):
        # enroll the student in the course
        self.personal_enrollments_api.create_personal_enrollment(
            objective.id, user.id, self.client
        )

    def expel_one_student(self, objective: Objective):
        # get all personal enrollments in this course objective
        skip = 0
        take = 10
        try:
            res = self.objectives_api.get_objective_personal_enrollments_by_query(
                objective.id,
                {
                    "skip": skip,
                    "take": take,
                    "requireTotalCount": True,
                },
                self.client,
            )
            if not res["data"]:
                raise ObjectivePersonalEnrollmentNotFoundException(
                    f"No personal enrollment in objective {objective.id}"
                )
            personal_enrollment_dict = random.choice(res["data"])
            self.personal_enrollments_api.delete_personal_enrollment_by_id(
                personal_enrollment_dict["id"], self.client
            )
        except ObjectivePersonalEnrollmentNotFoundException as e:
            logging.error(e.message)

    def select_one_student(self) -> User:
        # select a random student from mongodb
        # check student exists, otherwise select again
        user = None
        while user is None:
            user = self._select_one_student()
        return user

    def _select_one_student(self) -> User:
        username = random.choice(self.db_driver.find_usernames())
        skip = 0
        take = 10
        try:
            while True:
                res = self.users_api.get_users_by_query(
                    {
                        "skip": skip,
                        "take": take,
                        "requireTotalCount": True,
                        "filter": f'["username","contains","{username}"]',
                    },
                    self.client,
                )
                remaining_count = res["totalCount"] - take - skip
                users = res["data"]
                user_dict = next(
                    (user for user in users if user["username"] == username), None
                )
                skip += take
                if user_dict is not None:
                    user = User(user_dict)
                    self.db_driver.update_user(user)
                    return user
                if remaining_count <= 0:
                    raise UserNotFoundException(f"Username {username} doesn't exist.")
        except UserNotFoundException as e:
            logging.error(e.message)

    def select_one_objective(self) -> Objective:
        # select a random course objective
        objective = None
        while objective is None:
            objective = self._select_one_objective()
        return objective

    def _select_one_objective(self) -> Objective:
        course_code = random.choice(self.db_driver.find_courses_codes())
        skip = 0
        take = 10
        try:
            while True:
                res = self.objectives_api.get_objectives_by_query(
                    {
                        "skip": skip,
                        "take": take,
                        "requireTotalCount": True,
                        "filter": f'["code","contains","{course_code}"]',
                    },
                    self.client,
                )
                remaining_count = res["totalCount"] - take - skip
                objectives = res["data"]
                objective_dict = next(
                    (
                        objective
                        for objective in objectives
                        if objective["code"] == course_code
                    ),
                    None,
                )
                skip += take
                if objective_dict is not None:
                    objective = Objective(objective_dict)
                    self.db_driver.update_objective(objective)
                    return objective
                if remaining_count <= 0:
                    raise ObjectiveNotFoundException(
                        f"Objective code {course_code} doesn't exist."
                    )
        except ObjectiveNotFoundException as e:
            logging.error(e.message)

    def enroll_group(self):
        pass

    def update_objective(self):
        pass
