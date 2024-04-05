from .. import *
from typing import Callable, Union

import matplotlib.pyplot as plt
import numpy as np


POINTS_AMOUNT = 102
BOUNDS = (0, 20)


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

    plt.show()


def start() -> None:
    np_regressor = algorithms.NonparametricRegressor()

    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = np.sqrt(abscissa)

    abscissa = abscissa.reshape((POINTS_AMOUNT, 1))

    np_regressor.fit(abscissa[::3], ordinates[::3])

    _, axes = plt.subplots(figsize=(16, 8))

    predictions = np_regressor.predict(abscissa)
    visualize_results(axes, abscissa, ordinates, predictions)
    print(mse(predictions, ordinates), mae(predictions, ordinates), dc(predictions, ordinates))
