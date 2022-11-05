from app.drivers.database_driver import DatabaseDriver
from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.personal_enrollments_api import PersonalEnrollmentsAPI
from app.profiles.instructor import Instructor
from app.models.user import User
from app.models.objective.objective import Objective


def test_select_one_student():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    personal_enrollments_api = PersonalEnrollmentsAPI(db_driver)
    instructor = Instructor(
        db_driver, users_api, lms_users_api, objectives_api, personal_enrollments_api
    )
    user = instructor._select_one_student()
    assert type(user) is User


def test_select_one_objective():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    personal_enrollments_api = PersonalEnrollmentsAPI(db_driver)
    instructor = Instructor(
        db_driver, users_api, lms_users_api, objectives_api, personal_enrollments_api
    )
    objective = instructor._select_one_objective()
    assert type(objective) is Objective


def test_enroll_one_student():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    personal_enrollments_api = PersonalEnrollmentsAPI(db_driver)
    instructor = Instructor(
        db_driver, users_api, lms_users_api, objectives_api, personal_enrollments_api
    )
    user_to_enroll = instructor.select_one_student()
    objective_to_enroll = instructor.select_one_objective()
    count_before_enroll = objectives_api.get_objective_personal_enrollments_by_query(
        objective_to_enroll.id,
        {
            "skip": 0,
            "take": 0,
            "requireTotalCount": True,
        },
    )["totalCount"]
    instructor.enroll_one_student(user_to_enroll, objective_to_enroll)
    count_after_enroll = objectives_api.get_objective_personal_enrollments_by_query(
        objective_to_enroll.id,
        {
            "skip": 0,
            "take": 0,
            "requireTotalCount": True,
        },
    )["totalCount"]
    assert count_after_enroll == count_before_enroll + 1


def test_expel_one_student():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    personal_enrollments_api = PersonalEnrollmentsAPI(db_driver)
    instructor = Instructor(
        db_driver, users_api, lms_users_api, objectives_api, personal_enrollments_api
    )
    objective_to_expel = instructor.select_one_objective()
    count_before_expel = objectives_api.get_objective_personal_enrollments_by_query(
        objective_to_expel.id,
        {
            "skip": 0,
            "take": 0,
            "requireTotalCount": True,
        },
    )["totalCount"]
    instructor.expel_one_student(objective_to_expel)
    count_after_expel = objectives_api.get_objective_personal_enrollments_by_query(
        objective_to_expel.id,
        {
            "skip": 0,
            "take": 0,
            "requireTotalCount": True,
        },
    )["totalCount"]
    assert (
        count_after_expel == count_before_expel - 1
        or count_after_expel == 0
        and count_before_expel == 0
    )


def main():
    # test_select_one_student()
    # test_select_one_objective()
    # test_enroll_one_student()
    test_expel_one_student()


if __name__ == "__main__":
    main()
