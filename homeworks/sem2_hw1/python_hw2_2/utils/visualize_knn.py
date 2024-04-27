from typing import Optional
from itertools import cycle
from enum import Enum

import os
import matplotlib.pyplot as plt
import numpy as np


FIGSIZE = (16, 9)


class Colors(Enum):
    BLUE = "b"
    RED = "r"
    GREEN = "g"
    YELLOW = "y"
    BLACK = "k"
    WHITE = "w"


def visualize_scatter(
    points: np.ndarray,
    labels: np.ndarray,
    colors: Optional[list[Colors]] = None,
    axis: Optional[plt.Axes] = None,

) -> None:
    if colors is None:
        colors = list(Colors)

    colors_cycle = cycle([color.value for color in colors])
    labels_unique = np.unique(labels)

    if axis is None:
        figure, axis = plt.subplots(figsize=FIGSIZE)

    for label in labels_unique:
        label_mask = labels == label
        axis.scatter(*points[label_mask].T, color=next(colors_cycle))

    axis.grid(True)


def visualize_comparison(
    points: np.ndarray,
    prediction: np.ndarray,
    expectation: np.ndarray,
    path_to_save: str = "",
) -> None:
    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    ax1.set_title("prediction", fontsize=15, fontweight="bold", c="dimgray")
    ax2.set_title("expectation", fontsize=15, fontweight="bold", c="dimgray")

    visualize_scatter(points, prediction, axis=ax1)
    visualize_scatter(points, expectation, axis=ax2)

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
