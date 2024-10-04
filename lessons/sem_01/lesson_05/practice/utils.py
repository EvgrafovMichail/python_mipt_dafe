from typing import Callable

import matplotlib.pyplot as plt
import numpy as np

from regressors.regressor_abc import RegressorABC
from regressors.nonparametric_regressor import NonparametricRegressor
from regressors.lsm_regressor import RegressorLSM


K_NEIGHBOURS = 100
POINTS_AMOUNT = 1000
BOUNDS = (-10, 10)
FIGSIZE = (16, 8)


def visualize_results(
    axis: plt.Axes,
    abscissa: list,
    ordinates: list,
    predictions: list,
) -> None:
    """
    Визуализирует облако точек и полученную аппроксимацию.

    Args:
        axis: plt.Axes, на которой будут отрисованы графики.
        abscissa: абсциссы точек.
        prdinates: экспериментальные ординаты точек.
        predictions: ординаты точек, полученные в процессе аппроксимации.
    """
    axis.scatter(abscissa, ordinates, label="source", c="royalblue", s=1)
    axis.plot(abscissa, predictions, label="prediction", c="steelblue")

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()


def demonstrate(
    function: Callable[[np.ndarray], np.ndarray],
    regressors: list[RegressorABC],
) -> None:
    """
    Демонстрирует сравнение алгоритмов регрессии.

    Args:
        function: зависимость, для которой проводится сравнение.
        regressors: сравниваемые алгоритмы регрессии.
    """
    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = function(abscissa).tolist()
    abscissa = abscissa.tolist()

    for regressor in regressors:
        regressor.fit(abscissa, ordinates)

    _, axes = plt.subplots(1, len(regressors), figsize=FIGSIZE)
    axes: list[plt.Axes] = axes

    for ax, regressor in zip(axes, regressors):
        predictions = regressor.predict(abscissa)

        ax.set_title(type(regressor).__name__, fontweight="bold")
        visualize_results(ax, abscissa, ordinates, predictions)


def main() -> None:
    """Запускает демонстрацию."""
    functions = [linear, linear_modulated]
    regressors = [RegressorLSM(), NonparametricRegressor(K_NEIGHBOURS)]

    for function in functions:
        demonstrate(function, regressors)

    plt.show()


def linear(abscissa: np.ndarray) -> np.ndarray:
    """
    Вычисляет значения линейной функции f(x) = 5x + 1.

    Args:
        abscissa: значения абсцисс точек.

    Returns:
        Значения функции f(x) = 5x + 1 в точках abscissa.
    """
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    """
    Вычисляет значения модулированной функции f(x) = x * sin(x).

    Args:
        abscissa: значения абсцисс точек.

    Returns:
        Значения функции f(x) = x * sin(x) в точках abscissa.
    """
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise
