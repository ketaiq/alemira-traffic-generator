from enum import Enum, auto
import os

WORKLOAD_DIR = "app/workload"


class Weekday(Enum):
    """
    Weekday used for generating desired workload.
    """

    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()
    TEST = auto()


def get_workload_path(weekday: Weekday) -> str:
    weekday = weekday.name.capitalize()
    return os.path.join(WORKLOAD_DIR, f"workload_{weekday}.csv")
