"""
В этом модуле хранятся функции для применения МНК
"""
# import os.path
from types import NoneType
from typing import Optional
# from numbers import Real  # раскомментируйте при необходимости

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
        mismatch_strategy: MismatchStrategies = MismatchStrategies.CUT
) -> LSMDescription:
    """
    Функции для получения описания рассчитаной зависимости

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """
    global event_logger

    if (type(abscissa) is not list) or (type(ordinates) is not list):
        try:
            if type(abscissa) is not list:
                abscissa = list(abscissa)

            if type(ordinates) is not list:
                ordinates = list(ordinates)


        except TypeError:
            print("Bad data type(s)")

    if len(abscissa) <= 2 or len(ordinates) <= 2:
        raise ValueError("Not enough arguments")

    abscissa, ordinates = _process_mismatch(abscissa, ordinates, mismatch_strategy)
    LSMDescription = _get_lsm_description(abscissa, ordinates)

    return LSMDescription


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

    if type(lsm_description) is NoneType:
        lsm_description = get_lsm_description(abscissa, ordinates, )
        abscissa, ordinates = _process_mismatch(
            abscissa, ordinates,
                                                mismatch_strategy=MismatchStrategies.FALL)

    elif type(lsm_description) is not LSMDescription:
        raise TypeError("Wrong lsm_description type")

    line_predicted = [
        lsm_description.incline * x + lsm_description.shift
        for x in abscissa
    ]

    line_above = [
        (lsm_description.incline +
                   lsm_description.incline_error) * x +
                  lsm_description.shift +
                  lsm_description.shift_error
                  for x in abscissa]

    line_under = [(lsm_description.incline -
                   lsm_description.incline_error) * x +
                  lsm_description.shift -
                  lsm_description.shift_error
                  for x in abscissa]

    return LSMLines(
        abscissa,
        ordinates,
        line_predicted,
        line_above,
        line_under
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
    incline = lsm_description.incline
    shift = lsm_description.shift
    incline_err = lsm_description.incline_error
    shift_err = lsm_description.shift_error

    global PRECISION
    cool_statistic = '\n'.join(["LSM computing result".center(100, "="), '',
                                f'[INFO]: incline: {incline:.{PRECISION}f};',
                                f'[INFO]: shift: {shift:.{PRECISION}f};',
                                f'[INFO]: incline error: {incline_err:.{PRECISION}f};',
                                f'[INFO]: shift error: {shift_err:.{PRECISION}f};', '',
                                "====================".center(100, "=")])
    
    try: 
        with open(path_to_save, 'a') as file_to_save: 
            file_to_save.write(cool_statistic)

    except FileNotFoundError:
        return cool_statistic
    return cool_statistic


# служебная функция для валидации
def _is_valid_measurments(abscissa: list[float], ordinates: list[float]) -> bool:
    valid_data_types = [float, int]

    for i in range(len(ordinates)):
        if ((type(ordinates[i]) not in valid_data_types) or
                (type(abscissa[i]) not in valid_data_types)):
            try:
                ordinates[i] = float(ordinates[i])
                abscissa[i] = float(abscissa[i])
            except TypeError:
                print("Unsupported data type")
                return False
    return True


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
        abscissa: list[float], ordinates: list[float],
        mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger
    if len(abscissa) != len(ordinates):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError("Datalists have different length")
        if mismatch_strategy == MismatchStrategies.CUT:
            if len(abscissa) > len(ordinates):
                abscissa[:] = abscissa[:len(ordinates)]
            else:
                ordinates[:] = ordinates[:len(abscissa)]
        else:
            raise ValueError("Wrong mismatch_strategy value")
    return abscissa, ordinates


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
    sum_x_sqr = 0
    sum_xy = 0
    sum_disp_sqr = 0
    number_of_exp = len(ordinates)
    global event_logger, PRECISION

    if _is_valid_measurments(abscissa, ordinates):
        for i in range(number_of_exp):
            sum_xy += ordinates[i] * abscissa[i]
            sum_x_sqr += abscissa[i] ** 2

        x_mean = sum(abscissa) / number_of_exp
        y_mean = sum(ordinates) / number_of_exp
        xy_mean = sum_xy / number_of_exp
        x_sqr_mean = sum_x_sqr / number_of_exp

        incline = (xy_mean - x_mean * y_mean) / (x_sqr_mean - x_mean ** 2)
        shift = y_mean - incline * x_mean

        if number_of_exp == 2:
            incline_error_sqr = 0
            shift_error_sqr = 0
        else:
            for i in range(number_of_exp):
                sum_disp_sqr += (ordinates[i] - incline * abscissa[i] - shift) ** 2
            delta_y_sqr = sum_disp_sqr / (number_of_exp - 2)
            incline_error_sqr = delta_y_sqr / (number_of_exp * (x_sqr_mean - x_mean ** 2))
            shift_error_up = (x_sqr_mean * delta_y_sqr)
            shift_error_sqr = shift_error_up / (number_of_exp * (x_sqr_mean - x_mean ** 2))
    else:
        raise ValueError("Unsupported datatype")
    return LSMDescription(
        incline,
        shift,
        incline_error=incline_error_sqr ** 0.5,
        shift_error=shift_error_sqr ** 0.5
    )
