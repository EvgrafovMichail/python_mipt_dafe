from typing import Callable, Any

import matplotlib.pyplot as plt
import numpy as np
import os

from predictors.nonparamic_regr import NR
from quality_marks.metric import MAE, MSE, R_2
from utils import get_boxplot_outliers


K_NEIGHBOURS = 8
POINTS_AMOUNT = 1000
BOUNDS = (-10, 10)
FIGSIZE = (16, 8)


def visualize_results(
    axis: plt.Axes,
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    predictions: np.ndarray,
    corridor: bool = False,
    list_of_corridor: list[Any] = None
) -> None:
    predictions_outliers = get_boxplot_outliers(predictions, np.sort)
    abscissa_outliers = abscissa[np.argwhere(predictions_outliers == 1)]
    ordinates_outliers = ordinates[np.argwhere(predictions_outliers == 1)]

    axis.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)

    predictions = predictions[np.argwhere(predictions_outliers == 0)]
    abscissa1 = abscissa[np.argwhere(predictions_outliers == 0)]

    axis.scatter(abscissa_outliers, ordinates_outliers,
                 label='outliers', c='grey', s=1)

    axis.plot(abscissa1, predictions, label='prediction',
              c='violet', linewidth=1.5)
    if (corridor):
        axis.plot(list_of_corridor[0], list_of_corridor[1], label='limit', linestyle="--",
                  c='blue', linewidth=0.2)
        axis.plot(list_of_corridor[2], list_of_corridor[3], linestyle="--",
                  c='blue', linewidth=0.2)

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()


def get_demonstration(
    function: Callable[[np.ndarray], np.ndarray],
    regressors: list[NR],
    path_to_save: str = "",
) -> None:

    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = function(abscissa)

    for regressor in regressors:

        regressor.fit(abscissa, ordinates)

    figure, axes = plt.subplots(1, 2, figsize=(16, 8))

    for ax, regressor in zip(axes, regressors):
        predictions = regressor.predict(abscissa)

        ax.set_title(type(regressor).__name__, fontweight='bold')
        visualize_results(ax, abscissa, ordinates, predictions, True,
                          [abscissa, ordinates + 4, abscissa, ordinates - 4])
        print(f'MAE={MAE(predictions, ordinates):.4f}',
              f'MSE={MSE(predictions, ordinates):.4f}',
              f'R_2={R_2(predictions, ordinates):.4f}',
              sep='\n')
    if not path_to_save == "":
        save = ''
        if not os.path.exists(os.path.dirname(path_to_save)):
            raise FileNotFoundError(
                f"Directory '{os.path.dirname(path_to_save)}' does not exist.")
        elif os.path.exists(path_to_save):
            print(
                f"\n UserWarning: File '{path_to_save}' already exists."
                f" Overwriting it may lead to data loss. Do you want to continue? (y/n)")
            save = input()
            while save != 'y' and save != 'n' and save != '':
                print("wrong ans")
                save = input()
            if save != 'y':
                print("Aborting save.")
        if save != 'no':
            figure.savefig(path_to_save)

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
