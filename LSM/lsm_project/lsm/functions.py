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

#done
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

    # ваш код

    _is_valid_measurments(abscissa)
    _is_valid_measurments(ordinates)
    _process_mismatch(abscissa, ordinates, mismatch_strategy)

    avrx = sum(abscissa)/len(abscissa)
    avry = sum(ordinates)/len(ordinates)

    avrxy = 0
    avrsqrx = 0
    avrsqry = 0

    for i in range(len(abscissa)):
        avrxy += abscissa[i]*ordinates[i]
        avrsqrx += abscissa[i]**2
        avrsqry += ordinates[i]**2

    avrxy /= len(abscissa)
    avrsqrx /= len(abscissa)
    avrsqry /= len(abscissa)

    incline_ = (avrxy - avrx*avry)/(avrsqrx - avrx**2)
    shift_ = avry - incline_*avrx

    ordinates_error = (sum([(ordinates[i]-(incline_*abscissa[i]+shift_))**2 for i in range(len(abscissa))])/(len(abscissa)-2))**0.5
    incline_error_ = ((ordinates_error**2)/(len(abscissa)*(avrsqrx - avrx**2)))**0.5
    shift_error_ = ((ordinates_error**2) * avrsqrx /(len(abscissa)*(avrsqrx - avrx**2)))**0.5

    # эту строчку можно менять
    return LSMDescription(
        incline=incline_,
        shift=shift_,
        incline_error=incline_error_,
        shift_error=shift_error_
    )

#done
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

    # ваш код

    if not lsm_description:
        lsm_description = _get_lsm_description(abscissa, ordinates)
    elif not isinstance(lsm_description, LSMDescription):
        raise TypeError("invalid \"lsm_description\"")

    line_above_ = [lsm_description.shift + lsm_description.shift_error + (lsm_description.incline + lsm_description.incline_error)*x for x in abscissa]
    line_under_ = [lsm_description.shift - lsm_description.shift_error + (lsm_description.incline - lsm_description.incline_error)*x for x in abscissa]
    line_predicted_ = [lsm_description.shift + lsm_description.incline*x for x in abscissa]

    # эту строчку можно менять
    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_predicted_,
        line_above=line_above_,
        line_under=line_under_
    )

#done
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
    
    s = ("="*40 + "LSM computing result========================================\n\n"
         f"[INFO]: incline: {lsm_description.incline:.3f};\n"
         f"[INFO]: shift: {lsm_description.shift:.3f};\n"
         f"[INFO]: incline error: {lsm_description.incline_error:.3f};\n"
         f"[INFO]: shift error: {lsm_description.shift_error:.3f};\n\n"
         "="+"="*99)
    if path_to_save != '':
        with open(path_to_save, 'w') as f:
            f.write(s)
    # эту строчку можно менять
    return s


# служебная функция для валидации #done
def _is_valid_measurments(measurments: list[float]) -> None:
    # ваш код
    
    iter(measurments) #Проверка на итерируемый объект

    chkr = 1

    for i in measurments:
        chkr *= (isinstance(i, Real) or isinstance(i, int)) #Проверка на то, что в итерируемом объекте только числа

    if chkr == 0:
        raise ValueError("Values in measurments should be numbers")
    
    if len(measurments) < 3:
        raise ValueError("The amount of measurments should be atleast 3")

    # эту строчку можно менять
    return None


# служебная функция для обработки несоответствия размеров #done
def _process_mismatch(abscissa: list[float], ordinates: list[float], mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger

    # ваш код

    if len(abscissa) != len(ordinates):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError("Unable to fix mismatch of measurments")
        elif mismatch_strategy == MismatchStrategies.CUT:
            if len(abscissa) > len(ordinates):
                del abscissa[len(ordinates):len(abscissa)]
            else:
                del ordinates[len(abscissa):len(ordinates)]
        else:
            raise ValueError("Unpredicted value")

    # эту строчку можно менять
    return [abscissa], [ordinates]


# служебная функция для получения статистик #done
def _get_lsm_statistics(
    abscissa: list[float], ordinates: list[float], mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMStatistics:
    global event_logger, PRECISION

    # ваш код

    if len(abscissa) != len(ordinates):
        abscissa, ordinates = _process_mismatch(abscissa, ordinates, mismatch_strategy)

    _is_valid_measurments(abscissa)
    _is_valid_measurments(ordinates)

    avrx = sum(abscissa)/len(abscissa)
    avry = sum(ordinates)/len(ordinates)

    avrxy = 0
    avrsqrx = 0

    for i in range(len(abscissa)):
        avrxy += abscissa[i]*ordinates[i]
        avrsqrx += abscissa[i]**2

    avrxy /= len(abscissa)
    avrsqrx /= len(abscissa)

    # эту строчку можно менять
    return LSMStatistics(
        abscissa_mean=avrx,
        ordinate_mean=avry,
        product_mean=avrxy,
        abs_squared_mean=avrsqrx
    )


# служебная функция для получения описания МНК #done
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float], mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMDescription:
    global event_logger, PRECISION

    # ваш код

    stat = _get_lsm_statistics(abscissa, ordinates, mismatch_strategy)

    incline_ = (stat.product_mean - stat.abscissa_mean*stat.ordinate_mean)/(stat.abs_squared_mean - stat.abscissa_mean**2)
    shift_ = stat.ordinate_mean - incline_*stat.abscissa_mean

    ordinates_error_ = (sum([(ordinates[i]-(incline_*abscissa[i]+shift_))**2 for i in range(len(abscissa))])/(len(abscissa)-2))**0.5
    incline_error_ = ((ordinates_error_**2)/(len(abscissa)*(stat.abs_squared_mean - stat.abscissa_mean**2)))**0.5
    shift_error_ = ((ordinates_error_**2) * stat.abs_squared_mean /(len(abscissa)*(stat.abs_squared_mean - stat.abscissa_mean**2)))**0.5

    # эту строчку можно менять

    return LSMDescription(
        incline=incline_,
        shift=shift_,
        incline_error=incline_error_,
        shift_error=shift_error_
    )
