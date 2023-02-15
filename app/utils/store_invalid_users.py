from app.drivers.database_driver import db_driver
import pandas as pd


def main():
    invalid_users = db_driver.users.find()
    emails = []
    ids = []
    for user in invalid_users:
        emails.append(user["email"])
        ids.append(user["id"])
    df = pd.DataFrame(data={"id": ids, "email": emails})
    df.to_csv("data/invalid_users.csv", index=False)

if __name__ == "__main__":
    main()
