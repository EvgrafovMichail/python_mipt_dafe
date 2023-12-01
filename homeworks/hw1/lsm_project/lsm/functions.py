"""
В этом модуле хранятся функции для применения МНК
"""

import os
from typing import Optional
# from numbers import Real       # раскомментируйте при необходимости

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
    is_abscissa_corrected, abscissa = _is_valid_measurments(abscissa)
    is_ordinata_corrected, ordinates = _is_valid_measurments(ordinates)
    if is_abscissa_corrected and is_ordinata_corrected:
        if len(abscissa) != len(ordinates):
            if mismatch_strategy == MismatchStrategies.FALL:
                EventLogger.error(event_logger,
                                  'Не соответсвует количество значений Х и Y')
                raise RuntimeError
            elif mismatch_strategy == MismatchStrategies.CUT:
                abscissa = abscissa[:min(len(abscissa), len(ordinates))]
                ordinates = ordinates[:min(len(abscissa), len(ordinates))]
            else:
                EventLogger.error(event_logger,
                                  'Это никогда не произойдёт,'
                                  ' так как mismatch_strategy всего 2 вида')
                raise ValueError
    EventLogger.info(event_logger,
                     'Данные обработаны')

    amount_points = len(abscissa)
    x_average = sum(abscissa) / amount_points
    x_squres_average = sum(i ** 2 for i in abscissa) / amount_points
    y_average = sum(ordinates) / amount_points
    xy_average = sum(abscissa[i] * ordinates[i] for i in range(amount_points)) / amount_points

    incline = (xy_average - x_average * y_average) / (x_squres_average - x_average ** 2)
    shift = y_average - incline * x_average

    y_disperia = 0
    x_dispersia = 0
    for i in range(amount_points):
        y_disperia += (ordinates[i] - y_average) ** 2 / amount_points
        x_dispersia += (abscissa[i] - x_average) ** 2 / amount_points
    incline_error = ((y_disperia / x_dispersia - incline ** 2) / (amount_points - 2)) ** 0.5

    return LSMDescription(
        incline=incline,
        shift=shift,
        incline_error=incline_error,
        shift_error=incline_error * x_squres_average ** 0.5
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
    lsm_description_from_programm = get_lsm_description(abscissa, ordinates, MismatchStrategies.CUT)

    if lsm_description is not None:
        if any([format(lsm_description.incline, f'.{PRECISION}f') !=
                format(lsm_description_from_programm.incline, f'.{PRECISION}f'),
                format(lsm_description.shift, f'.{PRECISION}f') !=
                format(lsm_description_from_programm.shift, f'.{PRECISION}f'),
                format(lsm_description.incline_error, f'.{PRECISION}f') !=
                format(lsm_description_from_programm.incline_error, f'.{PRECISION}f'),
                format(lsm_description.shift_error, f'.{PRECISION}f') !=
                format(lsm_description_from_programm.shift_error, f'.{PRECISION}f')]):
            EventLogger.error(event_logger, 'Входное описание lsm е совпадает с рассчётами')
            raise TypeError
    lsm_description = get_lsm_description(abscissa, ordinates, MismatchStrategies.CUT)

    incline = lsm_description.incline
    shift = lsm_description.shift
    incline_error = lsm_description.incline_error
    shift_error = lsm_description.shift_error

    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=list(shift + incline * x for x in abscissa),
        line_above=list(shift + shift_error + (incline + incline_error) * x for x in abscissa),
        line_under=list(shift - shift_error + (incline - incline_error) * x for x in abscissa)
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

    incline = lsm_description.incline
    shift = lsm_description.shift
    incline_error = lsm_description.incline_error
    shift_error = lsm_description.shift_error

    report = ('LSM computing result'.center(100, '=') + '\n' + '\n'
              + f'[INFO]: incline: {format(incline, f".{PRECISION}f")};' + '\n' +
              f'[INFO]: shift: {format(shift, f".{PRECISION}f")};' + '\n' +
              f'[INFO]: incline error: {format(incline_error, f".{PRECISION}f")};' + '\n' +
              f'[INFO]: shift error: {format(shift_error, f".{PRECISION}f")};' + '\n' + '\n' +
              ''.center(80 + len('LSM computing result'), '='))

    if path_to_save:
        try:
            if os.path.exists(path_to_save):
                f = open(path_to_save, 'w')
                f.write(report)
                f.close()
            else:
                f = open(path_to_save, 'x')
                f.write(report)
                f.close()
        except:
            pass
    return report


# служебная функция для валидации
def _is_valid_measurments(measurments: list[float]) -> (bool, list[float]):
    if type(measurments) is list:
        if _only_real_numbers(measurments) and len(measurments) == 0:
            raise TypeError
        if _only_real_numbers(measurments) and len(measurments) > 2:
            return True, measurments
        raise ValueError

    elif type(measurments) is dict:
        key_list = measurments.keys()
        value_items = measurments.values()

        if _only_real_numbers(value_items) and len(value_items) > 2:
            return True, value_items
        if _only_real_numbers(key_list) and len(key_list) > 2:
            return True, key_list
        EventLogger.error(
            event_logger,
            'Удивительные вещи, подали словарь, но ни ключи,'
            ' ни значения не являются подходящими данными'
        )
        raise TypeError

    else:
        try:
            new_list = list(measurments)
            if _only_real_numbers(new_list) and len(new_list) > 2:
                return True, new_list
            raise ValueError
        except:
            EventLogger.error(
                event_logger,
                'Непонятный тип данных, невозможно представить в виде list[float]'
            )
            raise TypeError


def _only_real_numbers(measurments: list[float]) -> bool:
    for i in measurments:
        try:
            float(i)
        except:
            raise ValueError
    return True


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
