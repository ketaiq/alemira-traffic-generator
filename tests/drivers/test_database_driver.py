from app.drivers.database_driver import DatabaseDriver


def test_driver():
    driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    assert "admin" in driver.client.list_database_names()
    assert "config" in driver.client.list_database_names()
    assert "local" in driver.client.list_database_names()
    assert driver.client.address == ("localhost", 27017)


def main():
    test_driver()


if __name__ == "__main__":
    main()
