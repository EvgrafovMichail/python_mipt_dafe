import matplotlib.pyplot as plt
from enum_classes import Colors
from typing import Optional
from itertools import cycle
import numpy as np


def visual_regression(
        pred_points: np.ndarray,
        points: np.ndarray,
        mae: float,
        mse: float,
        rss: float,
        title: str,
):
    _, axis = plt.subplots(figsize=(16, 9))

    axis.scatter(
        points[:, 0],
        points[:, 1],
        label="Points",
        c="steelblue",
    )
    axis.plot(
        pred_points[:, 0],
        pred_points[:, 1],
        label="Regression",
        color="crimson",
    )

    axis.set_title(f"{title}\nMAE: {mae}, MSE: {mse}, rss: {rss}", fontsize=20)
    # axis.grid()
    plt.legend()
    plt.show()


def visual_knn(
    points: np.ndarray,
    real_labels: np.ndarray,
    pred_labels: np.ndarray,
    accuracy: float,
    colors: Optional[list[Colors]] = None,
):
    _, axis = plt.subplots(1, 2, figsize=(16, 9))

    unique_labels = np.unique(real_labels)

    if colors is None:
        colors = list(Colors)
    colors_cycle1 = cycle([color.value for color in colors])
    colors_cycle2 = cycle([color.value for color in colors])

    for label in unique_labels:
        real_labels_mask = real_labels == label
        axis[0].scatter(
            *points[real_labels_mask].T,
            color=next(colors_cycle1)
        )
        axis[0].set_title("Real", fontsize=18)

        pred_label_mask = pred_labels == label
        axis[1].scatter(
            *points[pred_label_mask].T,
            color=next(colors_cycle2)
        )
        axis[1].set_title(f"Predicted\n accuracy: {accuracy}", fontsize=18)

    plt.show()
