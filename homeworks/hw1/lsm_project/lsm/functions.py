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
    absc: list[float], ords: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMDescription:
    """
    Функции для получения описания рассчитаной зависимости

    :param: absc - значения абсцисс
    :param: ord - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """

    global event_logger

    _is_valid_measurments(absc)
    _is_valid_measurments(ords)
    _process_mismatch(absc, ords, mismatch_strategy)

    avr_x = sum(absc)/len(absc)
    avr_y = sum(ords)/len(ords)

    avr_xy = 0
    avr_sqr_x = 0
    avr_sqr_y = 0

    for i in range(len(absc)):
        avr_xy += absc[i]*ords[i]
        avr_sqr_x += absc[i]**2
        avr_sqr_y += ords[i]**2

    avr_xy /= len(absc)
    avr_sqr_x /= len(absc)
    avr_sqr_y /= len(absc)

    k = (avr_xy - avr_x*avr_y)/(avr_sqr_x - avr_x**2)
    b = avr_y - k*avr_x

    n = len(absc)

    y_error = (sum([(ords[i]-(k*absc[i] + b))**2 for i in range(n)])/(n-2))**0.5
    k_error = ((y_error ** 2) / (n * (avr_sqr_x - avr_x ** 2))) ** 0.5
    b_error = ((y_error ** 2) * avr_sqr_x / (n * (avr_sqr_x - avr_x**2)))**0.5

    return LSMDescription(
        incline=k,
        shift=b,
        incline_error=k_error,
        shift_error=b_error
    )


def get_lsm_lines(
    absc: list[float], ords: list[float],
    lsm_description: Optional[LSMDescription] = None
) -> LSMLines:
    """
    Функция для расчета значений функций с помощью результатов МНК

    :param: absc - значения абсцисс
    :param: ords - значение ординат
    :param: lsm_description - описание МНК

    :return: структура типа LSMLines
    """

    if not lsm_description:
        lsm_description = _get_lsm_description(absc, ords)
    elif not isinstance(lsm_description, LSMDescription):
        raise TypeError("invalid \"lsm_description\"")

    b = lsm_description.shift
    b_error = lsm_description.shift_error
    k = lsm_description.incline
    k_error = lsm_description.incline_error

    line_above_ = [b + b_error + (k + k_error)*x for x in absc]
    line_under_ = [b - b_error + (k - k_error)*x for x in absc]
    line_predicted_ = [b + k*x for x in absc]

    return LSMLines(
        abscissa=absc,
        ordinates=ords,
        line_predicted=line_predicted_,
        line_above=line_above_,
        line_under=line_under_
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

    s = ("="*40 + "LSM computing result========================================\n\n"
         f"[INFO]: incline: {lsm_description.incline:.3f};\n"
         f"[INFO]: shift: {lsm_description.shift:.3f};\n"
         f"[INFO]: incline error: {lsm_description.incline_error:.3f};\n"
         f"[INFO]: shift error: {lsm_description.shift_error:.3f};\n\n"
         "="+"="*99)
    if path_to_save != '':
        with open(path_to_save, 'w') as f:
            f.write(s)

    return s


# служебная функция для валидации #done
def _is_valid_measurments(measurments: list[float]) -> None:

    iter(measurments)  # Проверка на итерируемый объект

    chkr = 1

    for i in measurments:
        chkr *= (isinstance(i, Real))  # Проверка на то, что в итерируемом объекте только числа

    if chkr == 0:
        raise ValueError("Values in measurments should be numbers")

    if len(measurments) < 3:
        raise ValueError("The amount of measurments should be atleast 3")

    return None


# служебная функция для обработки несоответствия размеров
def _process_mismatch(absc: list[float], ords: list[float],
                      mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
                      ) -> tuple[list[float], list[float]]:
    global event_logger

    if len(absc) != len(ords):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError("Unable to fix mismatch of measurments")
        elif mismatch_strategy == MismatchStrategies.CUT:
            if len(absc) > len(ords):
                del absc[len(ords):len(absc)]
            else:
                del ords[len(absc):len(ords)]
        else:
            raise ValueError("Unpredicted value")

    return [absc], [ords]


# служебная функция для получения статистик
def _get_lsm_statistics(
    absc: list[float], ords: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
                        ) -> LSMStatistics:
    global event_logger, PRECISION

    if len(absc) != len(ords):
        absc, ords = _process_mismatch(absc, ords, mismatch_strategy)

    _is_valid_measurments(absc)
    _is_valid_measurments(ords)

    avr_x = sum(absc)/len(absc)
    avr_y = sum(ords)/len(ords)

    avr_xy = 0
    avr_sqr_x = 0

    for i in range(len(absc)):
        avr_xy += absc[i]*ords[i]
        avr_sqr_x += absc[i]**2

    avr_xy /= len(absc)
    avr_sqr_x /= len(absc)

    return LSMStatistics(
        abscissa_mean=avr_x,
        ordinate_mean=avr_y,
        product_mean=avr_xy,
        abs_squared_mean=avr_sqr_x
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
    absc: list[float], ords: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
                         ) -> LSMDescription:
    global event_logger, PRECISION

    stat = _get_lsm_statistics(absc, ords, mismatch_strategy)

    avr_x = stat.abscissa_mean
    avr_y = stat.ordinate_mean
    avr_sqr_x = stat.abs_squared_mean
    avr_xy = stat.product_mean

    k = (avr_xy - avr_x*avr_y)/(avr_sqr_x - avr_x**2)
    b = avr_y - k*avr_x
    n = len(absc)

    y_error = (sum([(ords[i]-(k*absc[i]+b))**2 for i in range(n)])/(n-2))**0.5
    k_error = ((y_error**2)/(n*(avr_sqr_x - avr_x**2)))**0.5
    b_error = ((y_error**2) * avr_sqr_x / (n*(avr_sqr_x - avr_x**2))) ** 0.5

    return LSMDescription(
        incline=k,
        shift=b,
        incline_error=k_error,
        shift_error=b_error
    )
