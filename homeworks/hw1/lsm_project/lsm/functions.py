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

    Measurments = _is_valid_measurments(abscissa, ordinates)

    Measurments = _process_mismatch(Measurments[0], Measurments[1], mismatch_strategy)

    return _get_lsm_description(Measurments[0], Measurments[1])


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
    if not (isinstance(lsm_description, LSMDescription) or lsm_description is None):
        raise TypeError
    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)

    Incline = lsm_description.incline
    Shift = lsm_description.shift
    Incline_error = lsm_description.incline_error
    Shift_error = lsm_description.shift_error

    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=[Incline * arg + Shift for arg in abscissa],
        line_above=[((Incline + Incline_error) * arg + (Shift + Shift_error)) for arg in abscissa],
        line_under=[((Incline - Incline_error) * arg + (Shift - Shift_error)) for arg in abscissa]
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

    font = "="
    report = '\n'.join([
        'LSM computing result'.center(100, font), '',
        f'[INFO]: incline: {lsm_description.incline:.{PRECISION}f};',
        f'[INFO]: shift: {lsm_description.shift:.{PRECISION}f};',
        f'[INFO]: incline error: {lsm_description.incline_error:.{PRECISION}f};',
        f'[INFO]: shift error: {lsm_description.shift_error:.{PRECISION}f};',
        '', ''.center(100, font)
    ])

    if path_to_save != '':
        with open(path_to_save, 'w') as f:
            f.write(report)

    return report


# служебная функция для валидации
def _is_valid_measurments(abscissa: list[float], ordinates: list[float]) -> list[float]:
    # ваш код
    def real_number_check(measurments: list[float]):
        for number in measurments:
            if not (isinstance(number, Real)):
                print(type(number))
                raise ValueError

    result = []
    for measurments in [abscissa, ordinates]:
        try:    # despair = отчаяние
            despair_measurments = list(measurments)
            if len(despair_measurments) < 3:
                raise ValueError
            real_number_check(despair_measurments)
            measurments = despair_measurments
        except:
            raise TypeError
        result.append(measurments)
    # эту строчку можно менять
    return result


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger

    # ваш код
    if len(ordinates) != len(abscissa):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError

        elif mismatch_strategy == MismatchStrategies.CUT:
            if len(abscissa) < len(ordinates):                      # Приравнивание их размеров
                del ordinates[len(abscissa):]
            else:
                del abscissa[len(ordinates):]

        else:
            raise ValueError

    result = [abscissa, ordinates]
    # эту строчку можно менять
    return result


# служебная функция для получения статистик
def _get_lsm_statistics(
    abscissa: list[float], ordinates: list[float]
) -> LSMStatistics:
    global event_logger, PRECISION

    # ваш код
    average_x = average_y = average_xy = average_x2 = 0                         # average_x = <x>
    len_input = len(abscissa)

    for iter in range(len_input):                            # считывание среднего из всех данных
        average_x += abscissa[iter] / len_input
        average_y += ordinates[iter] / len_input
        average_xy += abscissa[iter] * ordinates[iter] / len_input
        average_x2 += abscissa[iter] ** 2 / len_input

    # эту строчку можно менять
    return LSMStatistics(
        abscissa_mean=average_x,
        ordinate_mean=average_y,
        product_mean=average_xy,
        abs_squared_mean=average_x2
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global event_logger, PRECISION

    # ваш код
    statistic = _get_lsm_statistics(abscissa, ordinates)
    average_x = statistic.abscissa_mean
    average_y = statistic.ordinate_mean
    average_xy = statistic.product_mean
    average_x2 = statistic.abs_squared_mean
    len_input = len(abscissa)

    Incline = (average_xy - average_x * average_y) / (average_x2 - average_x ** 2)
    Shift = average_y-Incline*average_x

    delta_y2 = 0

    for i in range(len(abscissa)):
        delta_y2 += ((ordinates[i] - (Incline * abscissa[i] + Shift)) ** 2) / (len_input - 2)

    delta_Incline = (delta_y2 / (len_input * (average_x2 - average_x ** 2))) ** 0.5
    delta_Shift = (delta_y2 * average_x2 / (len_input * (average_x2 - average_x ** 2))) ** 0.5

    # эту строчку можно менять
    return LSMDescription(
        incline=Incline,
        shift=Shift,
        incline_error=delta_Incline,
        shift_error=delta_Shift
    )
