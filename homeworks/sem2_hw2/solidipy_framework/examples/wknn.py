from solidipy_mipt import accuracy, train_test_split
from solidipy_mipt.algorithms import WKNN

import sklearn.datasets as skd
import matplotlib.pyplot as plt
import numpy as np

from enum import Enum
from itertools import cycle

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


def start() -> None:
    points, labels = skd.make_moons(n_samples=400, noise=0.3)
    train_test_data = train_test_split(points, labels, train_ratio=0.8, shuffle=True)
    features_train, features_test, targets_train, targets_test = train_test_data

    wknn = WKNN()
    wknn.fit(features_train, targets_train)
    prediction = wknn.predict(features_test)
    visualize_comparison(features_test, prediction, targets_test)
    print(accuracy(prediction, targets_test))


if __name__ == "__main__":
    start()
