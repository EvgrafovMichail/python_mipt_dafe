"""
CPU computitions mock
"""

from time import time, sleep
from itertools import cycle

from modules_lesson.computitions.constants import (
    WHEEL_SYMBOLS,
    PAUSE_TIME,
    RESULT_MOCK,
)


CPU_TIME = 10               # время вычисления на СPU


def compute() -> None:
    wheel = cycle(WHEEL_SYMBOLS)
    time_start = time()

    while time() - time_start < CPU_TIME:
        print(f'\rComputing: {next(wheel)};', end='')
        sleep(PAUSE_TIME)

    print('')

    return RESULT_MOCK
