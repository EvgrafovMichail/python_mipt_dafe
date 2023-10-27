"""
В этом модуле хранятся функции для применения МНК
"""


from typing import Optional
from numbers import Real       # раскомментируйте при необходимости

from lsm_project.event_logger.event_logger import EventLogger

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)


PRECISION = 3                   # константа для точности вывода
event_logger = EventLogger()    # для логирования


def get_lsm_description(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMDescription:

    """
    Функции для получения описания рассчитаной зависимости

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """

    global event_logger
    if not isinstance(abscissa, list) or not isinstance(ordinates, list):
        try:
            abscissa = list(abscissa)
            ordinates = list(ordinates)
        except:
            raise TypeError
    if len(abscissa) <= 2 or len(ordinates) <= 2:
        raise ValueError
    if mismatch_strategy == MismatchStrategies.FALL and len(abscissa) != len(ordinates):
        raise RuntimeError
    elif mismatch_strategy == MismatchStrategies.CUT:
        abscissa = abscissa[:min(len(abscissa), len(ordinates))]
        ordinates = ordinates[:min(len(abscissa), len(ordinates))]
    elif not (mismatch_strategy == MismatchStrategies.FALL
              or mismatch_strategy == MismatchStrategies.CUT):
        raise ValueError
    for i in range(len(ordinates)):
        if (not isinstance(ordinates[i], Real)) or (not isinstance(abscissa[i], Real)):
            raise ValueError
    n = len(abscissa)
    aver_x = sum(abscissa) / n
    aver_y = sum(ordinates) / n
    aver_xy = sum([abscissa[i] * ordinates[i] for i in range(n)]) / n
    aver_xx = sum([elem ** 2 for elem in abscissa]) / n

    a = (aver_xy - aver_x * aver_y) / (aver_xx - aver_x ** 2)
    b = aver_y - a * aver_x
    sigm_y_sq = sum([(ordinates[i] - a * abscissa[i] - b) ** 2 for i in range(n)]) / (n - 2)
    sigm_a = (sigm_y_sq / (n * (aver_xx - aver_x ** 2))) ** 0.5
    sigm_b = (sigm_y_sq * aver_xx / (n * (aver_xx - aver_x ** 2))) ** 0.5

    return LSMDescription(
        incline=a,
        shift=b,
        incline_error=sigm_a,
        shift_error=sigm_b
    )


def get_lsm_lines(
    abscissa: list[float], ordinates: list[float],
    lsm_description: Optional[LSMDescription] = None
) -> LSMLines:
    """
    Функция для расчета значений функций с помощью результатов МНК

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: lsm_description - описание МНК

    :return: структура типа LSMLines
    """

    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates, MismatchStrategies.CUT)
    elif not isinstance(lsm_description, LSMDescription):
        raise TypeError
    line_predicted = []
    line_above = []
    line_under = []
    a_line_above = lsm_description.incline + lsm_description.incline_error
    a_line_under = lsm_description.incline - lsm_description.incline_error
    b_line_above = lsm_description.shift + lsm_description.shift_error
    b_line_under = lsm_description.shift - lsm_description.shift_error
    for elem in abscissa:
        line_predicted.append(lsm_description.incline * elem + lsm_description.shift)
        line_above.append(a_line_above * elem + b_line_above)
        line_under.append(a_line_under * elem + b_line_under)
    # эту строчку можно менять
    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_predicted,
        line_above=line_above,
        line_under=line_under
    )


def get_report(
    lsm_description: LSMDescription, path_to_save: str = ''
) -> str:
    """
    Функция для формирования отчета о результатах МНК

    :param: lsm_description - описание МНК
    :param: path_to_save - путь к файлу для сохранения отчета

    :return: строка - отчет определенного формата
    """
    global PRECISION
    printing = (
                "LSM computing result".center(100, "=") +
                "\n\n[INFO]: incline: {};\n[INFO]: shift: {};\n[INFO]: "
                "incline error: {};\n[INFO]: shift error: {};\n\n" + "=" * 100
                )
    incline = format(lsm_description.incline, '.3f')
    shift = lsm_description.shift
    incline_error = lsm_description.incline_error
    shift_error = lsm_description.shift_error
    if len(path_to_save):
        file = open(path_to_save, "w")
        file.write(printing.format(incline, shift, incline_error, shift_error))
        file.close()

    # эту строчку можно менять
    return printing.format(incline, shift, incline_error, shift_error)


# служебная функция для валидации
def _is_valid_measurments(measurments: list[float]) -> bool:
    # ваш код
    # эту строчку можно менять
    return False


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger

    # ваш код
    # эту строчку можно менять
    return [], []


# служебная функция для получения статистик
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


# служебная функция для получения описания МНК
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
