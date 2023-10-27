"""
В этом модуле хранятся функции для применения МНК
"""


from typing import Optional
from numbers import Real  # раскомментируйте при необходимости

from lsm_project.event_logger.event_logger import EventLogger

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)


PRECISION = 3  # константа для точности вывода
event_logger = EventLogger()  # для логирования


def get_lsm_description(
    abscissa: list[float],
    ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL,
) -> LSMDescription:
    """
    Функции для получения описания рассчитаной зависимости

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """

    global event_logger

    _is_valid_measurments(abscissa, ordinates, mismatch_strategy)
    abscissa, ordinates = _process_mismatch(abscissa, ordinates, mismatch_strategy)

    len_of_list = len(ordinates)
    avg_x = sum(abscissa) / len_of_list  # Вычисление incline, shift
    avg_y = sum(ordinates) / len_of_list
    avg_xy = 0
    avg_x_square = 0
    for x, y in zip(abscissa, ordinates):
        avg_xy += x * y
        avg_x_square += x**2
    avg_xy /= len_of_list
    avg_x_square /= len_of_list

    incline = (avg_xy - avg_x * avg_y) / (avg_x_square - avg_x**2)
    shift = avg_y - incline * avg_x

    intermediate_value = 0  # Вычисление погрешностей incline, shift
    for x, y in zip(abscissa, ordinates):
        intermediate_value += (y - incline * x - shift) ** 2
    y_error = intermediate_value / (len_of_list - 2)
    incline_error = (y_error / (len_of_list * (avg_x_square - avg_x**2))) ** 0.5
    shift_error = (
        y_error * avg_x_square / (len_of_list * (avg_x_square - avg_x**2))
    ) ** 0.5

    return LSMDescription(
        incline,
        shift,
        incline_error,
        shift_error,
    )


def get_lsm_lines(
    abscissa: list[float],
    ordinates: list[float],
    lsm_description: Optional[LSMDescription] = None,
) -> LSMLines:
    """
    Функция для расчета значений функций с помощью результатов МНК

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: lsm_description - описание МНК

    :return: структура типа LSMLines
    """

    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)
    elif not isinstance(lsm_description, LSMDescription):
        raise TypeError(f"unexpected lsm_description type: {type(lsm_description).__name__}")

    line_predicted = []
    line_above = []
    line_under = []
    for x in abscissa:
        line_predicted.append(lsm_description.incline * x + lsm_description.shift)
        line_above.append(
            (lsm_description.incline + lsm_description.incline_error) * x
            + lsm_description.shift
            + lsm_description.shift_error
        )
        line_under.append(
            (lsm_description.incline - lsm_description.incline_error) * x
            + lsm_description.shift
            - lsm_description.shift_error
        )

    return LSMLines(
        abscissa,
        ordinates,
        line_predicted,
        line_above,
        line_under,
    )


def get_report(lsm_description: LSMDescription, path_to_save: str = "") -> str:
    """
    Функция для формирования отчета о результатах МНК

    :param: lsm_description - описание МНК
    :param: path_to_save - путь к файлу для сохранения отчета

    :return: строка - отчет определенного формата
    """
    global PRECISION

    if not (isinstance(lsm_description, LSMDescription)) or lsm_description is None:
        raise TypeError(f"unexpected lsm_description type: {type(lsm_description).__name__}")

    string_legth = 100
    lsm_desc = lsm_description
    info = "\n".join(
        [
            "LSM computing result".center(string_legth, "="),
            "",
            f"[INFO]: incline: {lsm_desc.incline:.{PRECISION}f};",
            f"[INFO]: shift: {lsm_desc.shift:.{PRECISION}f};",
            f"[INFO]: incline error: {lsm_desc.incline_error:.{PRECISION}f};",
            f"[INFO]: shift error: {lsm_desc.shift_error:.{PRECISION}f};",
            "",
            "".center(string_legth, "="),
        ]
    )

    if len(path_to_save) > 0:
        with open(path_to_save, "w") as f:
            f.write(info)

    return info


# служебная функция для валидации
def _is_valid_measurments(
    abscissa: list[float],
    ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL,
) -> bool:
    try:
        abscissa = list(abscissa)
        ordinates = list(ordinates)
    except:
        raise TypeError()
    if any(
        [
            not isinstance(abscissa, list),
            not isinstance(ordinates, list),
        ]
    ):
        raise TypeError(
            f"unexpected measurement type: {type(abscissa).__name__, type(ordinates).__name__}"
            )
    if not isinstance(mismatch_strategy, MismatchStrategies):
        raise ValueError(f"unexpected mismatch_strategy type: {type(mismatch_strategy).__name__}")
    for list1 in (abscissa, ordinates):
        if len(list1) < 3:
            raise ValueError(f"unexpected list length: {len(list1)}")

    for list1 in (abscissa, ordinates):
        if any([not isinstance(number, Real) for number in list1]):
            raise ValueError("unexpected measurment value")

    return True


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
    abscissa: list[float],
    ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL,
) -> tuple[list[float], list[float]]:
    global event_logger

    if len(abscissa) == len(ordinates):
        return abscissa, ordinates
    elif mismatch_strategy == MismatchStrategies.FALL:
        raise RuntimeError()
    elif mismatch_strategy == MismatchStrategies.CUT:
        if len(abscissa) > len(ordinates):
            abscissa = abscissa[0:len(ordinates)]
        else:
            ordinates = ordinates[0:len(abscissa)]
    else:
        raise ValueError(f"unexpected mismatch_strategy type: {type(mismatch_strategy).__name__}")


# служебная функция для получения статистик
def _get_lsm_statistics(abscissa: list[float], ordinates: list[float]) -> LSMStatistics:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять
    return LSMStatistics(
        abscissa_mean=0, ordinate_mean=0, product_mean=0, abs_squared_mean=0
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять
    return LSMDescription(incline=0, shift=0, incline_error=0, shift_error=0)
