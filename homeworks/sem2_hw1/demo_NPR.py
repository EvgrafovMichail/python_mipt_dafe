from algorithm.np_regression import NPR
from metrics.grade_metric import MAE, MSE, R_2
from metrics.metric import Metric
from preprocessing import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable
import os


dir = os.path.dirname(os.path.abspath(__file__))


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
    axis.scatter(abscissa, ordinates, label='source', c='r', s=1)
    axis.plot(abscissa, predictions, label='prediction',
              c='royalblue', linewidth=1.5)

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()


def get_demonstration(
    function: Callable[[np.ndarray], np.ndarray],
    regressors: list[NPR],
) -> None:

    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = function(abscissa)

    X_train, X_test, Y_train, Y_test = train_test_split(
        abscissa,
        ordinates,
        shuffle=True,
        train_ratio=0.5
    )

    for regressor in regressors:

        regressor.fit(X_train, Y_train)

    _, axes = plt.subplots(1, 2, figsize=(16, 8))

    axes[0].set_title("NPR(l1)", fontweight='bold')
    axes[1].set_title("NPR(l2)", fontweight='bold')

    for ax, regressor in zip(axes, regressors):
        predictions = regressor.predict(X_train)
        mask = np.argsort(X_train)
        X_train = X_train[mask]
        Y_train = Y_train[mask]

        visualize_results(ax, X_train, Y_train, predictions)
        print(f'MAE={MAE(predictions, Y_train):.4f}',
              f'MSE={MSE(predictions, Y_train):.4f}',
              f'R_2={R_2(predictions, Y_train):.4f}',
              sep='\n')

    plt.savefig(f"{dir}/images/npr_train.png")

    _, axes = plt.subplots(1, 2, figsize=(16, 8))

    axes[0].set_title("NPR(l1)", fontweight='bold')
    axes[1].set_title("NPR(l2)", fontweight='bold')

    for ax, regressor in zip(axes, regressors):
        predictions = regressor.predict(X_test)
        mask = np.argsort(X_test)
        X_test = X_test[mask]
        Y_test = Y_test[mask]

        visualize_results(ax, X_test, Y_test, predictions)
        print(f'TEST_MAE={MAE(predictions, Y_test):.4f}',
              f'TEST_MSE={MSE(predictions, Y_test):.4f}',
              f'TEST_R_2={R_2(predictions, Y_test):.4f}',
              sep='\n')

    plt.savefig(f"{dir}/images/npr_test.png")


def main() -> None:
    functions = [linear, linear_modulated]
    regressors = [NPR(metric=Metric.l1), NPR()]

    get_demonstration(functions[1], regressors)


def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


if __name__ == "__main__":
    main()
