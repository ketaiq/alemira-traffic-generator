from enum import Enum


class Day(Enum):
    """
    Days used for experiment configuration. Each kind of day corresponds to
    different weights during traffic generation.
    """

    DAY_1 = 1
    DAY_2 = 2
    DAY_OTHER = 3
