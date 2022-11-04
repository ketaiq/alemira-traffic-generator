import time, random
from datetime import datetime, timedelta


def sleep_for_seconds(lower_bound: int, upper_bound: int):
    time.sleep(random.randrange(lower_bound, upper_bound))


def get_current_timestamp() -> int:
    return round(time.time() * 1000)


def get_current_formatted_time() -> str:
    return datetime.now().isoformat()[:-3] + "Z"


def get_future_formatted_time(days: int) -> str:
    time = datetime.now() + timedelta(days=days)
    return time.isoformat()[:-3] + "Z"
