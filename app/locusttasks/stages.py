from enum import Enum
from app.locusttasks.days import Day
from app.exceptions.unsupported import UnsupportedDayException
import logging

class Stage(Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"

def get_stage_by_day(day: Day):
    try:
        if day == Day.DAY_1 or day == Day.DAY_2:
            return Stage.FIRST
        elif day == Day.DAY_OTHER:
            return Stage.SECOND
        else:
            raise UnsupportedDayException(day)
    except UnsupportedDayException as e:
        logging.error(e.message)
