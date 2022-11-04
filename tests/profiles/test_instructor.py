from app.drivers.database_driver import DatabaseDriver
from app.apis.users_api import UsersAPI
from app.apis.lms_users_api import LmsUsersAPI
from app.apis.objectives_api import ObjectivesAPI
from app.profiles.instructor import Instructor
from app.models.user import User
from app.models.objective.objective import Objective


def test_select_one_student():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    instructor = Instructor(db_driver, users_api, lms_users_api, objectives_api)
    user = instructor.select_one_student()
    assert type(user) is User


def test_select_one_objective():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    users_api = UsersAPI()
    lms_users_api = LmsUsersAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    instructor = Instructor(db_driver, users_api, lms_users_api, objectives_api)
    objective = instructor.select_one_objective()
    assert type(objective) is Objective


def main():
    # test_select_one_student()
    test_select_one_objective()


if __name__ == "__main__":
    main()
