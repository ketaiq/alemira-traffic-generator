from app.utils.string import gen_random_name, gen_random_email, gen_random_middle_name
from app.models.detail import Detail


class User:
    def __init__(self, user: dict):
        self.id = user["id"]
        self.username = user["username"]
        self.email = user["email"]
        self.firstName = user["firstName"]
        self.middleName = user["middleName"]
        self.lastName = user["lastName"]
        self.externalId = user["externalId"]
        self.tenant = user["tenant"]
        self.details = user["details"]

    @staticmethod
    def gen_random_user() -> "User":
        firstName = gen_random_name()
        middleName = gen_random_middle_name()
        lastName = gen_random_name()
        email = gen_random_email()
        username = email
        details = Detail.gen_random_detail()
        return User(
            {
                "id": None,
                "externalId": None,
                "firstName": firstName,
                "middleName": middleName,
                "lastName": lastName,
                "email": email,
                "username": username,
                "details": details,
                "tenant": None,
            }
        )


def main():
    print(vars(User.gen_random_user()))


if __name__ == "__main__":
    main()
