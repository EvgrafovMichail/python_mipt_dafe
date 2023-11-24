from typing import Callable, Union

import matplotlib.pyplot as plt
import numpy as np


from regressors.nonparametric_regressor import NonparametricRegressor
from regressors.lsm_regressor import RegressorLSM

from common.log import EventLogger


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
    axis.plot(abscissa, predictions, label='prediction', c='steelblue')

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()


def get_demonstration(
    function: Callable[[np.ndarray], np.ndarray],
    regressors: list[Union[RegressorLSM, NonparametricRegressor]],
) -> None:
    event_logger = EventLogger(function.__name__)
    event_logger.info('obtain linear function data')

    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = function(abscissa).tolist()
    abscissa = abscissa.tolist()

    event_logger.info('start fitting regressors')

    for regressor in regressors:
        event_logger.info(f'fit {type(regressor).__name__}')
        regressor.fit(abscissa, ordinates)

    event_logger.info('prepare figure')
    _, axes = plt.subplots(1, 2, figsize=(16, 8))

    event_logger.info('start getting predictions')

    for ax, regressor in zip(axes, regressors):
        event_logger.info(f'get prediction for {type(regressor).__name__}')
        predictions = regressor.predict(abscissa)

        ax.set_title(type(regressor).__name__, fontweight='bold')
        visualize_results(ax, abscissa, ordinates, predictions)

    plt.show()


def main() -> None:
    functions = [linear, linear_modulated]
    regressors = [RegressorLSM(), NonparametricRegressor()]

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
