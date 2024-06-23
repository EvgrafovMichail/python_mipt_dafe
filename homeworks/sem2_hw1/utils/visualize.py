import matplotlib.pyplot as plt
import numpy as np
import os
import warnings

from itertools import cycle
from enum import Enum

FIGSIZE = (16, 9)


class Colors(Enum):
    BLUE = "blue"
    CYAN = "cyan"
    ORANGE = "orange"
    GREEN = "green"
    PURPLE = "purple"
    RED = "red"


def visualize_scatter(
    points: np.ndarray,
    labels: np.ndarray,
    colors: list[str] = None,
    axis: plt.Axes = None,
) -> None:
    if colors is None:
        colors = [color.value for color in Colors]

    colors_cycle = cycle(colors)

    labels_unique = np.unique(labels)

    if axis is None:
        fig, axis = plt.subplots(figsize=FIGSIZE)

    for label in labels_unique:
        label_mask = labels == label
        axis.scatter(*points[label_mask].T, color=next(colors_cycle))

    axis.grid(True)


def visualize_comparison(
    points: np.ndarray,
    prediction: np.ndarray,
    expectation: np.ndarray,
    colors: list[str] = None,
    path_to_save: str = '',
) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    ax1.set_title("Prediction", fontsize=15, fontweight="bold", color="dimgray")
    ax2.set_title("Expectation", fontsize=15, fontweight="bold", color="dimgray")

    visualize_scatter(points, prediction, colors=colors, axis=ax1)
    visualize_scatter(points, expectation, colors=colors, axis=ax2)

    if path_to_save:
        if os.path.isdir(path_to_save):
            warnings.warn("File already exists at the specified path, overwriting it.")
        plt.savefig(path_to_save)

    plt.show()
