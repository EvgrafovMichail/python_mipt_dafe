import time
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np

from main import NREGR, KNN
from main import MAE, MSE, rr, train_test_split, accuracy

import sklearn.datasets as skd

from utils import (
    visualize_comparison,
    freeze_random_seed,
)

K_NEIGHBOURS = 5
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
        regressors: list[NREGR],
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

        print(f"MSE = {MSE(predictions, ordinates)}",
              f"MAE = {MAE(predictions, ordinates)}",
              f"rr = {rr(predictions, ordinates)}",
              sep='\n')

    plt.show()


def main() -> None:
    functions = [linear, linear_modulated]
    regressors = [NREGR(5, "l1"), NREGR(5, 'l1')]

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


if __name__ == '__main__':
    freeze_random_seed()
    points, labels = skd.make_moons(n_samples=400, noise=0.3)
    # visualize_scatter(points, labels)

    points_train, points_test, labels_train, labels_test = train_test_split(
        features=points,
        targets=labels,
        shuf=True,
        train_ratio=0.8,
    )

    knn = KNN(5, 'l2')
    knn.fit(points_train, labels_train)
    prediction = knn.predict(points_test)

    visualize_comparison(points_test, prediction, labels_test)

    accuracy_score = accuracy(prediction, labels_test)
    print(f"knn accuracy: {accuracy_score}")

    time.sleep(10)

    main()
