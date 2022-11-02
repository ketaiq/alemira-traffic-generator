import time, random


def sleep_for_seconds(lower_bound: int, upper_bound: int):
    time.sleep(random.randrange(lower_bound, upper_bound))
