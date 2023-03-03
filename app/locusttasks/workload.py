from enum import Enum
import os

WORKLOAD_DIR = "app/workload"

class Weekday(Enum):
    """
    Weekday used for generating desired workload.
    """
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

def get_workload_path(weekday: Weekday) -> str:
    weekday = weekday.name.capitalize()
    return os.path.join(WORKLOAD_DIR, f"workload_{weekday}.csv")
