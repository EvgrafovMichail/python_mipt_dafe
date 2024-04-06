from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


from predictors.nonparamic_regr import NR
from quality_marks.metric import MAE, MSE, R_2


K_NEIGHBOURS = 8
POINTS_AMOUNT = 1000
BOUNDS = (-10, 10)
FIGSIZE = (16, 8)


def visualize_results(
    axis: plt.Axes,
    abscissa: list,
    ordinates: list,
    predictions: list,
) -> None:
    axis.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)
    axis.plot(abscissa, predictions, label='prediction',
              c='violet', linewidth=1.5)

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()


def get_demonstration(
    function: Callable[[np.ndarray], np.ndarray],
    regressors: list[NR],
) -> None:

    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = function(abscissa)

    for regressor in regressors:

        regressor.fit(abscissa, ordinates)

    _, axes = plt.subplots(1, 2, figsize=(16, 8))

    for ax, regressor in zip(axes, regressors):
        predictions = regressor.predict(abscissa)

        ax.set_title(type(regressor).__name__, fontweight='bold')
        visualize_results(ax, abscissa, ordinates, predictions)
        print(f'MAE={MAE(predictions, ordinates):.4f}',
              f'MSE={MSE(predictions, ordinates):.4f}',
              f'R_2={R_2(predictions, ordinates):.4f}',
              sep='\n')

    plt.show()


def main() -> None:
    functions = [linear, linear_modulated]
    regressors = [NR(metric='l2'), NR()]

    for function in functions:

        get_demonstration(function, regressors)


def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


main()
