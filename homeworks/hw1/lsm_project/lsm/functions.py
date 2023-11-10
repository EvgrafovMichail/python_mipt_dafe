"""
В этом модуле хранятся функции для применения МНК
"""

from typing import Optional
from numbers import Real
from pathlib import Path
from inspect import stack

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)

from lsm_project.lsm.math import mean, line
from lsm_project.event_logger.event_logger import EventLogger
from lsm_project.event_logger.utils import log_errors


PRECISION = 3                 # константа для точности вывода
event_loger = EventLogger()


@log_errors(event_loger)
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
        raise ValueError(
            f"unexpected mismatch strategy type: "
            f"{type(mismatch_strategy).__name__}"
        )

    try:
        abscissa, ordinates = _process_mismatch(
            abscissa=abscissa,
            ordinates=ordinates,
            mismatch_strategy=mismatch_strategy
        )
    except (ValueError, RuntimeError) as e:
        raise type(e) from e
    else:
        event_loger.debug(
            f"{stack()[0][3]} || "
            f"mismatch was successfully processed: "
            f"{abscissa=} length={len(abscissa)}; "
            f"{ordinates=} length={len(ordinates)};"
        )

    description = _get_lsm_description(abscissa, ordinates)
    event_loger.debug(
        f"{stack()[0][3]} || "
        f"description was successfully created: {description}"
    )

    return description


@log_errors(event_loger)
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

    func_name = stack()[0][3]

    if not lsm_description:
        try:
            lsm_description = _get_lsm_description(abscissa, ordinates)
        except (ValueError, RuntimeError) as e:
            raise e

    if not isinstance(lsm_description, LSMDescription):
        raise TypeError(
            f"invalid lsm description: "
            f"{type(lsm_description).__name__}"
        )

    if not _is_valid_data(abscissa, ordinates):
        raise ValueError(
            "invalid data: expected 3 or more real number measurement but got "
            f"abscissa: {len(abscissa)}; "
            f"ordinates: {len(ordinates)};"
        )

    if len(abscissa) != len(ordinates):
        event_loger.debug(
            f"{stack()[0][3]} || "
            f"mismatch length of abscissa and ordinates: "
            f"{abscissa=} length={len(abscissa)}; "
            f"{ordinates=} length={len(ordinates)};"
        )

        try:
            abscissa, ordinates = _process_mismatch(
                abscissa=abscissa,
                ordinates=ordinates,
                mismatch_strategy=MismatchStrategies.CUT
            )
        except (ValueError, RuntimeError) as e:
            raise e
        else:
            event_loger.debug(
                f"{stack()[0][3]} || "
                f"mismatch was successfully processed: "
                f"{abscissa=} length={len(abscissa)}; "
                f"{ordinates=} length={len(ordinates)};"
            )

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

    lsm_line = LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_predicted,
        line_above=line_above,
        line_under=line_under,
    )
    event_loger.debug(
        f"{func_name} || "
        f"lsm line was successfully created: {lsm_line}"
    )

    return lsm_line


@log_errors(event_loger)
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
        f"{label:=^100}\n"
        "\n"
        f"[INFO]: incline: {lsm_description.incline:.{PRECISION}f};\n"
        f"[INFO]: shift: {lsm_description.shift:.{PRECISION}f};\n"
        f"[INFO]: incline error: {lsm_description.incline_error:.{PRECISION}f};\n"
        f"[INFO]: shift error: {lsm_description.shift_error:.{PRECISION}f};\n"
        "\n"
        f"{footer:=^100}"
    )

    if path_to_save:
        path_to_save = Path(path_to_save)
        exist = path_to_save.exists()

        with open(path_to_save.absolute(), "w") as file:
            if not exist:
                event_loger.info(
                    f"{stack()[0][3]} || "
                    f"{path_to_save.absolute()} was successfully created"
                )

            file.write(report)

    return report


# служебная функция для валидации измерения
def _is_valid_measurements(
        measurements: list[float]
) -> bool:
    return all(isinstance(m, Real) for m in measurements) and measurements


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
@log_errors(event_loger)
def _process_mismatch(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    if not _is_valid_data(abscissa, ordinates):
        raise ValueError(
            "invalid data: expected 3 or more real number measurement but got "
            f"abscissa: {len(abscissa)}; "
            f"ordinates: {len(ordinates)};"
        )

    if len(abscissa) == len(ordinates):
        return abscissa, ordinates

    match mismatch_strategy:
        case MismatchStrategies.FALL:
            raise RuntimeError(
                f"quantity of abscissa and ordinates isn`t equal: "
                f"abscissa: {len(abscissa)}; "
                f"ordinates: {len(ordinates)}"
            )

        case MismatchStrategies.CUT:
            if len(abscissa) > len(ordinates):
                return abscissa[:len(ordinates)], ordinates

            return abscissa, ordinates[:len(abscissa)]

        case _:
            raise ValueError(
                "unexpected mismatch strategy type: "
                f"{type(mismatch_strategy).__name__}"
            )


# служебная функция для получения статистик
@log_errors(event_loger)
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

    statistics = LSMStatistics(
        abscissa_mean=abscissa_mean,
        ordinate_mean=ordinates_mean,
        product_mean=product_mean,
        abscissa_squared_mean=abscissa_squared_mean,
    )

    return statistics


# служебная функция для получения описания МНК
@log_errors(event_loger)
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    if not abscissa or not ordinates:
        raise ValueError("empty measurements")
    if len(abscissa) != len(ordinates):
        raise RuntimeError(
                f"quantity of abscissa and ordinates isn`t equal: "
                f"abscissa: {len(abscissa)}; "
                f"ordinates: {len(ordinates)}"
        )

    try:
        statistics = _get_lsm_statistics(abscissa, ordinates)
        event_loger.debug(
            f"{stack()[0][3]} || "
            f"statistics was successfully created: {statistics}"
        )

        coefficients = _calculate_coefficients(statistics, abscissa, ordinates)
        event_loger.debug(
            f"{stack()[0][3]} || "
            f"coefficients was successfully calculated"
        )
    except ValueError as e:
        raise e
    else:
        return LSMDescription(*coefficients)


# служебная функция для расчета коэффициентов МНК
def _calculate_coefficients(
        data: LSMStatistics, abscissa: list[float], ordinates: list[float]
) -> tuple[float, float, float, float]:
    incline = (
            (data.product_mean - data.abscissa_mean*data.ordinate_mean) /
            (data.abscissa_squared_mean - data.abscissa_mean**2)
    )

    shift = data.ordinate_mean - incline * data.abscissa_mean

    ordinates_dispersion = (
            sum([(y - incline*x - shift)**2 for x, y in zip(abscissa, ordinates)]) /
            (len(abscissa) - 2)
    )

    incline_dispersion = (
            ordinates_dispersion /
            (len(abscissa) * (data.abscissa_squared_mean - data.abscissa_mean**2))
    )

    shift_dispersion = incline_dispersion * data.abscissa_squared_mean

    return incline, shift, incline_dispersion**0.5, shift_dispersion**0.5
