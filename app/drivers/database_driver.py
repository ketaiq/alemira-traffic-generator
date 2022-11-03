from urllib.parse import quote_plus
from pymongo import MongoClient
from app.models.user import User
from app.models.objective.objective import Objective


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

    def insert_one_course(self, course: dict):
        self.courses.insert_one(course)

    def insert_one_objective(self, objective: Objective):
        self.objectives.insert_one(objective.to_dict_for_database())

    def update_objective(self, objective: Objective):
        self.objectives.update_one(
            {"id": objective.id}, {"$set": objective.to_dict_for_database()}
        )

    def update_password(self, user: User):
        self.users.update_one({"id": user.id}, {"$set": {"password": user.password}})

    def update_user(self, user: User):
        self.users.update_one({"id": user.id}, {"$set": user.to_dict_for_database()})
