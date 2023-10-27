"""
В этом модуле хранятся функции для применения МНК
"""


from typing import Optional
from numbers import Real       # раскомментируйте при необходимости

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)

from lsm_project.utils.math import mean, line
from lsm_project.utils.error import log_errors


PRECISION = 3   # константа для точности вывода


@log_errors
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

    if not isinstance(mismatch_strategy, MismatchStrategies):
        raise ValueError(f"unexpected mismatch strategy type: "
                         f"{type(mismatch_strategy).__name__}")

    try:
        abscissa, ordinates = _process_mismatch(
            abscissa=abscissa,
            ordinates=ordinates,
            mismatch_strategy=mismatch_strategy
        )
    except (ValueError, RuntimeError) as e:
        raise e

    return _get_lsm_description(abscissa, ordinates)


@log_errors
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

    if not lsm_description:
        try:
            lsm_description = _get_lsm_description(abscissa, ordinates)
        except (ValueError, RuntimeError) as e:
            raise e

    if not isinstance(lsm_description, LSMDescription):
        raise TypeError(f"invalid lsm description: "
                        f"{type(lsm_description).__name__}")

    try:
        abscissa, ordinates = _process_mismatch(
            abscissa=abscissa,
            ordinates=ordinates,
            mismatch_strategy=MismatchStrategies.CUT
        )
    except (ValueError, RuntimeError) as e:
        raise e

    line_predicted = line(
        lsm_description.incline,
        lsm_description.shift,
        abscissa
    )

    line_above = line(
        lsm_description.incline + lsm_description.incline_error,
        lsm_description.shift + lsm_description.shift_error,
        abscissa
    )

    line_under = line(
        lsm_description.incline - lsm_description.incline_error,
        lsm_description.shift - lsm_description.shift_error,
        abscissa
    )

    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_predicted,
        line_above=line_above,
        line_under=line_under,
    )


@log_errors
def get_report(
    lsm_description: LSMDescription, path_to_save: str = ''
) -> str:
    """
    Функция для формирования отчета о результатах МНК

    :param: lsm_description - описание МНК
    :param: path_to_save - путь к файлу для сохранения отчета

    :return: строка - отчет определенного формата
    """

    label = "LSM computing result"
    footer = ""
    report = (
        f"{label:.^100}"
        f"[INFO]: incline:{lsm_description.incline}"
        f"[INFO]: shift:{lsm_description.incline}"
        f"[INFO]: incline:{lsm_description.incline}"
        f"[INFO]: incline:{lsm_description.incline}"
        f"{footer:.^100}"
    )
    return 'report'


# служебная функция для валидации измерения
def _is_valid_measurements(
        measurements: list[float]
) -> bool:
    return all([isinstance(m, Real) for m in measurements]) and measurements


# служебная функция для валидации данных
def _is_valid_data(
        abscissa: list[float], ordinates: list[float]
) -> bool:
    return all([
        _is_valid_measurements(abscissa),
        _is_valid_measurements(ordinates),
        len(abscissa) > 2,
        len(ordinates) > 2,
    ])


# служебная функция для обработки несоответствия размеров
@log_errors
def _process_mismatch(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    if not _is_valid_data(abscissa, ordinates):
        raise ValueError("invalid data: expected 3 or more real number measurement")

    if len(abscissa) == len(ordinates):
        return abscissa, ordinates

    match mismatch_strategy:
        case MismatchStrategies.FALL:
            raise RuntimeError(f"quantity of abscissa and ordinates isn`t equal: "
                               f"{len(abscissa)=} {len(ordinates)=}")

        case MismatchStrategies.CUT:
            if len(abscissa) > len(ordinates):
                return abscissa[:len(ordinates)], ordinates

            return abscissa, ordinates[:len(abscissa)]

        case _:
            raise ValueError("unexpected mismatch strategy type: "
                             f"{type(mismatch_strategy).__name__}")


# служебная функция для получения статистик
@log_errors
def _get_lsm_statistics(
    abscissa: list[float], ordinates: list[float]
) -> LSMStatistics:
    try:
        abscissa_mean = mean(abscissa)
        ordinates_mean = mean(ordinates)

        product = list(map(
            lambda x: x[0] * x[1],
            zip(abscissa, ordinates)
        ))
        product_mean = mean(product)

        abscissa_squared = list(map(lambda x: x**2, abscissa))
        abscissa_squared_mean = mean(abscissa_squared)
    except ZeroDivisionError:
        raise ValueError("empty or zero measurements")

    return LSMStatistics(
        abscissa_mean=abscissa_mean,
        ordinate_mean=ordinates_mean,
        product_mean=product_mean,
        abscissa_squared_mean=abscissa_squared_mean,
    )


# служебная функция для получения описания МНК
@log_errors
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    if not abscissa or not ordinates:
        raise ValueError("empty measurements")
    if len(abscissa) != len(ordinates):
        raise RuntimeError(f"quantity of abscissa and ordinates isn`t equal: "
                           f"{len(abscissa)=} {len(ordinates)=}")

    try:
        statistics = _get_lsm_statistics(abscissa, ordinates)
    except ValueError as e:
        raise e
    else:
        return _calculate_coefficients(statistics, abscissa, ordinates)


# служебная функция для расчета коэффициентов МНК
def _calculate_coefficients(
        data: LSMStatistics, abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global PRECISION

    incline = round(
        (data.product_mean - data.abscissa_mean*data.ordinate_mean) /
        (data.abscissa_squared_mean - data.abscissa_mean**2),
        PRECISION,
    )

    shift = round(
        data.ordinate_mean - incline * data.abscissa_mean,
        PRECISION,
    )

    ordinates_dispersion = round(
        sum([(y - incline*x - shift)**2 for x, y in zip(abscissa, ordinates)]) /
        (len(abscissa) - 2),
        PRECISION,
    )

    incline_dispersion = round(
        ordinates_dispersion /
        len(abscissa) * (data.abscissa_squared_mean - data.abscissa_mean**2),
        PRECISION,
    )

    shift_dispersion = round(
        incline_dispersion * data.abscissa_squared_mean,
        PRECISION,
    )

    return LSMDescription(
        incline=incline,
        shift=shift,
        incline_error=incline_dispersion**0.5,
        shift_error=shift_dispersion**0.5,
    )
