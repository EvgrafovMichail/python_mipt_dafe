"""
В этом модуле хранятся функции для применения МНК
"""


from typing import Optional
# from numbers import Real       # раскомментируйте при необходимости

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
    # Проверки
    # 1) Оба входа - листы, по возможности привести к листу
    # 2) Длина одинакова

    # Вычисления <xy> <x> <y> <x^2>
    sumx = sumy = sumxy = sumx2 = 0

    leninput = len(abscissa)
    for iter in range(leninput): # считывание среднего из всех данных
        sumx += abscissa[iter] / leninput
        sumy += ordinates[iter] / leninput
        sumxy += abscissa[iter] * ordinates[iter] / leninput
        sumx2 += abscissa[iter] ** 2 / leninput
    
    Incline = (sumxy - sumx * sumy) / (sumx2 - sumx ** 2) # a
    Shift = sumy - Incline * sumx # b
    
    sumDispy = 0
    for iter in range(leninput): # счёт оценки дисперсии зависимой величины
        sumDispy += (ordinates[iter] - Incline * abscissa[iter] - Shift) ** 2 / (leninput-2)
    
    DispIncline = sumDispy / (leninput * (sumx2 - sumx ** 2)) # Дельта a
    DispShift = DispIncline * sumx2 / (leninput * (sumx2 - sumx ** 2)) # Дельта b

    global event_logger # ???
    
    return LSMDescription(
        incline=Incline,
        shift=Shift,
        incline_error=DispIncline,
        shift_error=DispShift
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

    # Проверки
    # 1) Необязательный аргумент
    # Вычисления
    data = get_lsm_description(abscissa, ordinates, True) # Изменить True на что-то из проверки

    Incline = data.incline
    Shift = data.shift

    def value(arg): # Функция определяет значение f(x)
        nonlocal Incline, Shift
        return Incline * arg + Shift

    leninput = len(abscissa)
    incline_error = data.incline_error
    shift_error = data.shift_error

    Line_Predict = [0] * leninput
    Line_Above = [0] * leninput
    Line_Under = [0] * leninput

    for iter in range(leninput): # Счет значений функций с входных данных
        Line_Predict[iter] = value(abscissa[iter])
        Line_Above[iter] = value(abscissa[iter] + incline_error) + shift_error
        Line_Under[iter] = value(abscissa[iter] - incline_error) - shift_error

    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=Line_Predict,
        line_above=Line_Above,
        line_under=Line_Under
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

    # ваш код
    # эту строчку можно менять
    return 'report'


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
