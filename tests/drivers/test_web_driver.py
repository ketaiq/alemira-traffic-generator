from app.drivers.web_driver import WebDriver
from app.models.user import User
import pytest
from selenium.common.exceptions import TimeoutException


def test_reset_password():
    web_driver = WebDriver()
    user = User(email="test@email.com", password="tW5$lA")
    with pytest.raises(TimeoutException):
        web_driver.reset_password(
            "https://identity.alms.dev.alemira.com/Account/ResetPassword?code=Q2ZESjhFRXVhK2tabmN4S21UWTNDNHV1dkEwUWc4TDdHRUpPL1RYcG5VV2cybm42ZWlsbGkvMW4xZm0vWTJOODJSTVRDV1pWWW5RUk45TnNxc0Y4R1NWSzhoNCtDNTI5cm1QNUtHSE9sakZLNDlzR0V3bEFIdkljUVFMZzd5b3NIcllsQmhtOVd6THV3dnZVUVdrUWRmbGx2UkdTcUZKTXRRZE1JRWwvVENIZWg5RTN2LzdXaUVNKzA2bG9uRloyQjE0OHhTZHRpRURINjRodVdHNCt5M0hUamltRndJS1crVVRjTGJxNWc5aTlWTEhr&amp;returnUrl=https%3a%2f%2f3.alemira.com",
            user,
        )


def main():
    test_reset_password()


if __name__ == "__main__":
    main()
