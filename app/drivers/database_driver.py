from urllib.parse import quote_plus
from pymongo import MongoClient
from app.models.user import User


class DatabaseDriver:
    def __init__(self, host: str, username: str, password: str):
        uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
        self.client = MongoClient(uri)
        self.db = self.client["alemira"]
        self.users = self.db["users"]

    def insert_one_user(self, user: dict):
        self.users.insert_one(user)

    def update_password(self, user: "User"):
        self.users.update_one({"id": user.id}, {"$set": {"password": user.password}})
