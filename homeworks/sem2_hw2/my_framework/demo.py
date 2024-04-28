from preprocessing.preprocessing import train_test_split
from grade.metrics import MSE, MAE, R_in_square, accuracy
from visualize.visualize_regressor import visualize_regressor
from algorithms.non_param_regressor import NonparametricRegressor
from algorithms.wknn import Wknn

import sklearn.datasets as skd

import matplotlib.pyplot as plt
import numpy as np

from enum import Enum
from itertools import cycle

POINTS_AMOUNT = 100
BOUNDS = (0, 10)
FIGSIZE = (16, 9)


def visualize_results(
    abscissa: list,
    ordinates: list,
    predictions: list,
) -> None:
    _, axis = plt.subplots(figsize=FIGSIZE)
    axis.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)
    axis.plot(abscissa, predictions, label='prediction', c='steelblue')

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()

    plt.show()


def get_np_regression():

    np_regressor = NonparametricRegressor()

    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = np.sin(abscissa)

    abscissa = abscissa.reshape((POINTS_AMOUNT, 1))

    np_regressor.fit(
        abscissa[::3],
        ordinates[::3] +
        np.random.random(ordinates[::3].shape[0]) *
        np.random.randint(-1, 2, ordinates[::3].shape[0])
    )

    prediction = np_regressor.predict(abscissa[::3])

    indeces = np.argsort(np.sum(abscissa[::3], axis=-1))
    X_test = abscissa[::3][indeces]
    y_test = ordinates[::3][indeces]
    prediction = prediction[indeces]

    print(
        MSE(prediction, y_test),
        MAE(prediction, y_test),
        R_in_square(prediction, y_test)
    )
    visualize_regressor(X_test, y_test, prediction, error=np.random.randint(1,2,X_test.shape[0]))


FIGSIZE = (16, 9)


class Colors(Enum):
    BLUE = "b"
    RED = "r"


def visualize_scatter(
    points: np.ndarray,
    labels: np.ndarray,
    colors: list[Colors] | None = None,
    axis: plt.Axes | None = None,
) -> None:
    if colors is None:
        colors = list(Colors)

    colors_cycle = cycle([color.value for color in colors])
    labels_unique = np.unique(labels)

    if axis is None:
        _, axis = plt.subplots(figsize=FIGSIZE)

    for label in labels_unique:
        label_mask = labels == label
        axis.scatter(*points[label_mask].T, color=next(colors_cycle))

    axis.grid(True)


def visualize_comparison(
    points: np.ndarray,
    prediction: np.ndarray,
    expectation: np.ndarray,
) -> None:
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    ax1.set_title("prediction", fontsize=15, fontweight="bold", c="dimgray")
    ax2.set_title("expectation", fontsize=15, fontweight="bold", c="dimgray")

    visualize_scatter(points, prediction, axis=ax1)
    visualize_scatter(points, expectation, axis=ax2)

    plt.show()


def get_wknn():
    points, labels = skd.make_moons(n_samples=400, noise=0.3)
    train_test_data = train_test_split(
        points,
        labels,
        train_ratio=0.4,
        shuffle=False
    )
    x_train, x_test, y_train, y_test = train_test_data

    wknn = Wknn()
    wknn.fit(x_train, y_train)
    prediction = wknn.predict(x_test)
    print(prediction)
    visualize_comparison(x_test, prediction, y_test)
    print(accuracy(prediction, y_test))


flag = False

if __name__ == "__main__":
    if (flag):
        get_np_regression()
    else:
        get_wknn()
