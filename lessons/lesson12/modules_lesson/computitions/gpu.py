"""
GPU computitions mock
"""

from time import time, sleep
from itertools import cycle

from modules_lesson.computitions.constants import (
    WHEEL_SYMBOLS,
    PAUSE_TIME,
    RESULT_MOCK,
)


GPU_TIME = 2                # время вычисления на GPU


def compute() -> None:
    wheel = cycle(WHEEL_SYMBOLS)
    time_start = time()

    while time() - time_start < GPU_TIME:
        print(f'\rComputing: {next(wheel)};', end='')
        sleep(PAUSE_TIME)

    print('')

    return RESULT_MOCK
