from typing import Optional
from numbers import Real

from event_logger.event_logger import EventLogger

from lsm.enumerations import MismatchStrategies
from lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)


PRECISION = 3
event_logger = EventLogger()


def get_lsm_description(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMDescription:
    global event_logger

    # ваш код
    # эту строчку можно менять
    return LSMDescription(
        incline=0,
        shift=0,
        incline_error=0,
        shift_error=0
    )


def get_lsm_lines(
    abscissa: list[float], ordinates: list[float],
    lsm_description: Optional[LSMDescription] = None
) -> LSMLines:
    # ваш код
    # эту строчку можно менять
    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=ordinates,
        line_above=ordinates,
        line_under=ordinates
    )


def get_report(
    lsm_description: LSMDescription, path_to_save: str = ''
) -> str:
    global PRECISION
    
    # ваш код
    # эту строчку можно менять
    return 'report'


def _is_valid_measurments(measurments: list[float]) -> bool:
    # ваш код
    # эту строчку можно менять
    return False


def _process_mismatch(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger

    # ваш код
    # эту строчку можно менять
    return [], []


def _get_lsm_statistics(
    abscissa: list[float], ordinates: list[float]
) -> LSMStatistics:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять
    return LSMStatistics(
        abscissa_mean=0,
        ordinate_mean=0,
        product_mean=0,
        abs_squared_mean=0
    )


def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять
    return LSMDescription(
        incline=0,
        shift=0,
        incline_error=0,
        shift_error=0
    )
