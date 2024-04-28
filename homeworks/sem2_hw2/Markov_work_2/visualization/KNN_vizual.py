from __future__ import absolute_import
from typing import Optional
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
import warnings
import os

FIGSIZE = (16, 9)


class Colors:
    pass


def visualize_scatter(
    points: np.ndarray,
    labels: np.ndarray,
    colors: Optional[list[Colors]],
    axis: Optional[plt.Axes] = None,
) -> None:

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
    colors: list[Colors] = None,
    path_to_save: str = "",
) -> None:
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    ax1.set_title("prediction", fontsize=15, fontweight="bold", c="dimgray")
    ax2.set_title("expectation", fontsize=15, fontweight="bold", c="dimgray")

    visualize_scatter(points, prediction, colors, axis=ax1)
    visualize_scatter(points, expectation, colors, axis=ax2)

    if str != "":  # сохраняем изображение
        if os.path.exists(path_to_save):
            warnings.warn("Warning a file with the specified name exists")
        plt.savefig(path_to_save)
