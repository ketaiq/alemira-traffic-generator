from app.apis.endpoint import EndPoint
import requests
from app.database.driver import Driver
from app.models.user import User


class AccountResetPasswordAPI(EndPoint):
    def __init__(self, driver: Driver):
        self.headers = {"accept": "*/*"}
        self.driver = driver

    def reset_password(
        self,
        url: str,
        user: User,
    ):
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        print(r.text)
        code = ""
        return_url = ""
        verification_token = ""
        user.reset_password()
        payload = {
            "Input.Code": code,
            "Input.ReturnUrl": return_url,
            "Input.Email": user.email,
            "Input.Password": user.password,
            "Input.ConfirmPassword": user.password,
            "__RequestVerificationToken": verification_token,
        }
        r = requests.post(
            url,
            headers=self.headers,
            data=payload,
        )
        r.raise_for_status()
        print(r.text)
