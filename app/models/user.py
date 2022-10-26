from app.utils.string import (
    gen_random_name,
    gen_random_email,
    gen_random_middle_name,
    gen_random_bool,
)
from app.models.model import Model
from app.models.detail import Detail
from app.models.tenant import Tenant


class User(Model):
    FIELD_NAMES = (
        "id",
        "externalId",
        "firstName",
        "middleName",
        "lastName",
        "email",
        "username",
        "details",
        "tenant",
    )
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
        if self.details is not None:
            self.details = Detail(self.details)
        if self.tenant is not None:
            self.tenant = Tenant(self.tenant)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "User":
        user_dict = dict()
        user_dict["firstName"] = gen_random_name()
        user_dict["middleName"] = gen_random_middle_name()
        user_dict["lastName"] = gen_random_name()
        user_dict["email"] = gen_random_email()
        user_dict["username"] = user_dict["email"]
        user_dict["details"] = Detail.gen_random_object()
        return User(user_dict)

    def gen_random_update(self):
        changed = False
        if gen_random_bool():
            self.firstName = gen_random_name()
            changed = True
        if gen_random_bool():
            self.lastName = gen_random_name()
            changed = True
        if gen_random_bool() or not changed:
            self.middleName = gen_random_middle_name()
        if gen_random_bool():
            self.email = gen_random_email()
            self.username = self.email
        if gen_random_bool():
            self.details = self.details.gen_random_update()

    @classmethod
    def filter_original_users(cls, users: list) -> list:
        return [user for user in users if user["email"] not in cls.RESERVED_EMAILS]


def main():
    user = User.gen_random_object()
    print(vars(user))
    print(user.to_dict())


if __name__ == "__main__":
    main()
