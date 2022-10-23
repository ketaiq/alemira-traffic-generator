from app.utils.string import (
    gen_random_name,
    gen_random_email,
    gen_random_middle_name,
    gen_random_bool,
)
from app.models.model import Model
from app.models.detail import Detail


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

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.FIELD_NAMES,
            *args,
            **kwargs,
        )

    @staticmethod
    def gen_random_object() -> "User":
        user_dict = dict()
        user_dict["firstName"] = gen_random_name()
        user_dict["middleName"] = gen_random_middle_name()
        user_dict["lastName"] = gen_random_name()
        user_dict["email"] = gen_random_email()
        user_dict["username"] = user_dict["email"]
        user_dict["details"] = Detail.gen_random_object()
        return User(user_dict)


def main():
    user = User.gen_random_object()
    print(vars(user))
    print(user.to_dict())


if __name__ == "__main__":
    main()
