from app.utils.time import (
    get_current_timestamp,
    get_current_formatted_time,
    get_future_formatted_time,
)
from datetime import datetime, timedelta


def test_get_current_timestamp():
    assert get_current_timestamp() > 1667467256996


def test_get_current_formatted_time():
    time_str = get_current_formatted_time().rstrip("Z")
    time = datetime.fromisoformat(time_str)
    assert time > datetime(2022, 11, 1)


def test_get_future_formatted_time():
    time_str = get_future_formatted_time(180).rstrip("Z")
    time = datetime.fromisoformat(time_str)
    assert time < datetime.now() + timedelta(days=180)


def main():
    test_get_current_formatted_time()
    test_get_future_formatted_time()


if __name__ == "__main__":
    main()
