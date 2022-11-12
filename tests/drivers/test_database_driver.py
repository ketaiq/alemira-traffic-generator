from app.drivers.database_driver import db_driver


def test_driver():
    assert "admin" in db_driver.client.list_database_names()
    assert "config" in db_driver.client.list_database_names()
    assert "local" in db_driver.client.list_database_names()
    assert db_driver.client.address == ("localhost", 27017)


def main():
    test_driver()


if __name__ == "__main__":
    main()
