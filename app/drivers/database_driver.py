from urllib.parse import quote_plus
from pymongo import MongoClient
from app.models.user import User


class DatabaseDriver:
    def __init__(self, host: str, username: str, password: str):
        uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
        self.client = MongoClient(uri)
        self.db = self.client["alemira"]
        self.users = self.db["users"]
        self.courses = self.db["courses"]

    def insert_one_user(self, user: dict):
        self.users.insert_one(user)

    def insert_one_course(self, course: dict):
        self.courses.insert_one(course)

    def update_password(self, user: User):
        self.users.update_one({"id": user.id}, {"$set": {"password": user.password}})

    def update_user(self, user: User):
        self.users.update_one({"id": user.id}, {"$set": user.to_dict_for_database()})
