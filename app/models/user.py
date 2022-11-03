from app.utils.string import (
    gen_random_name,
    gen_random_email,
    gen_random_password,
)
from app.models.model import Model
from app.models.detail import Detail
from app.models.tenant import Tenant
import random, copy, logging
from app.exceptions import UnsupportedModeException
from app.models.dict_mode import DictMode


class User(Model):
    FIELD_NAMES = (
        "id",
        "externalId",
        "firstName",
        "middleName",
        "lastName",
        "email",
        "username",
        "password",
        "details",
        "tenant",
    )
    FIELD_FOR_CREATING = (
        "externalId",
        "firstName",
        "middleName",
        "lastName",
        "email",
        "username",
        "details",
    )
    FIELD_FOR_UPDATING = (
        "externalId",
        "firstName",
        "middleName",
        "lastName",
        "email",
        "username",
        "details",
    )
    FIELD_FOR_LOGIN = ("username", "password")
    RESERVED_EMAILS = (
        "chen@company.com",
        "alice@company.com",
        "bob@company.com",
        "jane@company.com",
        "elena@company.com",
        "david@company.com",
        "alex@company.com",
        "lucy@company.com",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.FIELD_NAMES,
            *args,
            **kwargs,
        )
        if self.details is not None and type(self.details) is dict:
            self.details = Detail(self.details)
        if self.tenant is not None and type(self.tenant) is dict:
            self.tenant = Tenant(self.tenant)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "User":
        email = username = gen_random_email()
        return User(
            {
                "firstName": gen_random_name(),
                "middleName": gen_random_name() if random.choice([True, False]) else "",
                "lastName": gen_random_name(),
                "email": email,
                "username": username,
                "details": Detail.gen_random_object(),
                "externalId": "",
            }
        )

    def gen_random_update(self) -> "User":
        user = copy.deepcopy(self)
        while user == self:
            user.firstName = (
                gen_random_name() if random.choice([True, False]) else user.firstName
            )
            user.lastName = (
                gen_random_name() if random.choice([True, False]) else user.lastName
            )
            user.middleName = (
                gen_random_name() if random.choice([True, False]) else user.middleName
            )
            user.email = (
                gen_random_email() if random.choice([True, False]) else user.email
            )
            user.username = user.email
            user.details = user.details.gen_random_update()
        return user

    @classmethod
    def filter_original_users(cls, users: list) -> list:
        return [user for user in users if user["email"] not in cls.RESERVED_EMAILS]

    def reset_password(self):
        self.password = gen_random_password()

    def to_dict(self, mode: DictMode):
        try:
            if mode is DictMode.CREATE:
                fields = self.FIELD_FOR_CREATING
            elif mode is DictMode.UPDATE:
                fields = self.FIELD_FOR_UPDATING
            elif mode is DictMode.DATABASE:
                fields = self.FIELD_NAMES
            elif mode is DictMode.LOGIN:
                fields = self.FIELD_FOR_LOGIN
            else:
                raise UnsupportedModeException(f"Mode {mode} is not supported.")
        except UnsupportedModeException as e:
            logging.error(e.message)
        user_dict = {}
        for field in fields:
            value = getattr(self, field)
            if type(value) is Detail:
                value = value.__dict__
            user_dict[field] = value
        return user_dict

    def to_dict_for_creating(self) -> dict:
        return self.to_dict(DictMode.CREATE)

    def to_dict_for_updating(self) -> dict:
        return self.to_dict(DictMode.UPDATE)

    def to_dict_for_database(self) -> dict:
        return self.to_dict(DictMode.DATABASE)

    def to_dict_for_login(self) -> dict:
        return self.to_dict(DictMode.LOGIN)

    def __eq__(self, other):
        for key in self.FIELD_NAMES:
            if getattr(self, key) != getattr(other, key):
                return False
        return True


def main():
    user = User.gen_random_object()
    print(vars(user))
    print(user.to_dict())
    new_user = user.gen_random_update()
    print(new_user.to_dict())
    user1 = {
        "firstName": "A",
        "middleName": "",
        "lastName": "A",
        "email": "email",
        "username": "username",
        "details": Detail(city="city", school="school", grade="grade"),
    }
    user2 = {
        "firstName": "A",
        "middleName": "",
        "lastName": "A",
        "email": "email",
        "username": "username",
        "details": Detail(city="city", school="school", grade="grade"),
    }
    print(user1 == user2)


if __name__ == "__main__":
    main()
