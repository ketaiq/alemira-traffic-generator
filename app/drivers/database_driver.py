from urllib.parse import quote_plus
from pymongo import MongoClient
from app.models.user import User
from app.models.objective.objective import Objective
from app.models.activity.activity import Activity
from app.models.role import Role


class DatabaseDriver:
    def __init__(self, host: str, username: str, password: str):
        uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
        self.client = MongoClient(uri)
        self.db = self.client["alemira"]
        self.users = self.db["users"]
        self.courses = self.db["courses"]
        self.objectives = self.db["objectives"]

    def insert_one_user(self, user: User):
        self.users.insert_one(user.to_dict_for_database())

    def insert_one_course(self, course: Activity):
        self.courses.insert_one(course.to_dict_for_database())

    def insert_one_objective(self, objective: Objective):
        self.objectives.insert_one(objective.to_dict_for_database())

    def update_objective(self, objective: Objective):
        objective_dict = objective.to_dict_for_database()
        objective_dict.pop("id", None)
        self.objectives.update_one({"id": objective.id}, {"$set": objective_dict})

    def update_password(self, user: User):
        self.users.update_one({"id": user.id}, {"$set": {"password": user.password}})

    def update_user(self, user: User):
        user_dict = user.to_dict_for_database()
        user_dict.pop("_role", None)
        self.users.update_one({"id": user.id}, {"$set": user_dict})

    def update_course(self, course: Activity):
        self.courses.update_one(
            {"id": course.id}, {"$set": course.to_dict_for_database()}
        )

    def check_objective_by_code(self, objective: Objective) -> bool:
        return (
            True
            if self.objectives.find_one({"code": objective.code}) is not None
            else False
        )

    def check_course_by_code(self, course: Activity) -> bool:
        return (
            True if self.courses.find_one({"code": course.code}) is not None else False
        )

    def check_user_by_id(self, user: User) -> bool:
        return True if self.users.find_one({"id": user.id}) is not None else False

    def find_student_usernames(self) -> list:
        return self.users.find({"_role": Role.STUDENT.value}).distinct("username")

    def find_courses_codes(self) -> list:
        return self.courses.find().distinct("code")

    def find_admin_users(self) -> list:
        return list(self.users.find({"_role": Role.ADMIN.value}))

    def find_instructor_users(self) -> list:
        return list(self.users.find({"_role": Role.INSTRUCTOR.value}))

    def find_student_users(self) -> list:
        return list(self.users.find({"_role": Role.STUDENT.value}))


db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
