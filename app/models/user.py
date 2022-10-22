class User:
    def __init__(self, user: dict):
        self.id = user["id"]
        self.username = user["username"]
        self.email = user["email"]
        self.first_name = user["firstName"]
        self.middle_name = user["middleName"]
        self.last_name = user["lastName"]
        self.external_id = user["externalId"]
        self.tenant = user["tenant"]