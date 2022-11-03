import time, random


def sleep_for_seconds(lower_bound: int, upper_bound: int):
    time.sleep(random.randrange(lower_bound, upper_bound))


def get_current_timestamp() -> int:
    return round(time.time() * 1000)
