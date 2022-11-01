from app.models.mail_message import MailMessage


def test_get_reset_password_url():
    m = MailMessage(
        {
            "id": "ae0c5ce0-d690-4ba0-94cc-93c0ba94d176",
            "toName": None,
            "toAddress": "asdasdasd@qwe.com",
            "subject": "Welcome to SIT Alemira Platform",
            "textBody": None,
            "htmlBody": "An account was created for you on the SIT Alemira platform. To start using it, please set a password that is at least 6 symbols long and includes at least one upper- and lower-case letter, one digit and special character. <a href='https://identity.alms.dev.alemira.com/Account/ResetPassword?code=Q2ZESjhKWGhmWWJnVkNGQmpNSDdKeTZxb3NBY0pGRTByeDFUaXpKYWllZHJ6Vk94WDdqVjVDTUpiNUJWKzlhcXJvdzNxV0s1TDhGWHdIQndkTDJJdmNUTUdJZ2szQXRoT3ZqakJvS3ZnRUhKTExaUnlRVnNhVXlWUjVpQ2JQWitUSndQdjBZTFIzSkFFVW5mVm1CSmo2NzZZanhXdzRBUXp6dmNMU3VLNTJmaEgwQVR2NVZ1OUpmMkRwbjdBN1Y0TFBLY0JjODBEcUFLNnFPZEllZEVOelJybnhnc2EvYmtDbTZpcjJIelpoT2Z4TUhO&amp;returnUrl=https%3a%2f%2f3.alemira.com'>Click here to set a password</a>.",
            "created": "2022-10-23T09:25:41.439216Z",
            "modified": "2022-10-23T09:25:42.258861Z",
            "state": 2,
        }
    )
    assert (
        m.get_reset_password_url()
        == "https://identity.alms.dev.alemira.com/Account/ResetPassword?code=Q2ZESjhKWGhmWWJnVkNGQmpNSDdKeTZxb3NBY0pGRTByeDFUaXpKYWllZHJ6Vk94WDdqVjVDTUpiNUJWKzlhcXJvdzNxV0s1TDhGWHdIQndkTDJJdmNUTUdJZ2szQXRoT3ZqakJvS3ZnRUhKTExaUnlRVnNhVXlWUjVpQ2JQWitUSndQdjBZTFIzSkFFVW5mVm1CSmo2NzZZanhXdzRBUXp6dmNMU3VLNTJmaEgwQVR2NVZ1OUpmMkRwbjdBN1Y0TFBLY0JjODBEcUFLNnFPZEllZEVOelJybnhnc2EvYmtDbTZpcjJIelpoT2Z4TUhO&amp;returnUrl=https%3a%2f%2f3.alemira.com"
    )


def main():
    test_get_reset_password_url()


if __name__ == "__main__":
    main()
