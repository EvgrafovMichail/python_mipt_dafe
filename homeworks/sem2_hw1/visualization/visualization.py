from typing import Optional, Any
import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np

from add_classes.enum_classes import Colors
from visualization.simple_graphs import (
    draw_box,
    draw_hist,
    draw_violin,
    draw_scatter
)
from algorithms.help_functions import save_file


def visual_regression(
        pred_points: np.ndarray,
        points: np.ndarray,
        error: np.ndarray = None,
        *,
        mae: float,
        mse: float,
        rss: float,
        title: str,
        path_to_save: str = "",
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

    if not (error is None):
        if pred_points.shape[0] != error.shape[0]:
            raise ValueError("Predicted points and error shapes mismatch")

        axis.plot(
            pred_points[:, 0],
            pred_points[:, 1] + error,
            label="Sigma-corridor",
            linestyle="dashed",
            color="pink",
        )
        axis.plot(
            pred_points[:, 0],
            pred_points[:, 1] - error,
            linestyle="dashed",
            color="pink",
        )

    axis.set_title(f"{title}\nMAE: {mae}, MSE: {mse}, rss: {rss}", fontsize=20)
    # axis.grid()
    plt.legend()

    save_file(path_to_save)

    plt.show()


def visual_knn(
    points: np.ndarray,
    real_labels: np.ndarray,
    pred_labels: np.ndarray,
    *,
    accuracy: float,
    colors: Optional[list[Colors]] = None,
    path_to_save: str = "",
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

    save_file(path_to_save)

    plt.show()


def visualize_distribution(
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: Any,
    *,
    path_to_save: str = "",
) -> None:
    if not (isinstance(data, np.ndarray)):
        raise ValueError("data must be a np.ndarray")

    if not (isinstance(axis, (list, plt.Axes))):
        raise ValueError("Axis must be a list of 3 axes or 1 axis")

    if not (isinstance(path_to_save, str)):
        raise ValueError("path_to_save must be a str")

    if not (data.ndim == 1 or data.shape[-1] == 2):
        raise ValueError("inappropriate data value")

    functions = {
        "hist": draw_hist,
        "violin": draw_violin,
        "boxplot": draw_box,
    }

    if not (diagram_type in functions):
        raise ValueError(f"{diagram_type} doesn't exist")

    draw_func = functions[diagram_type]

    if isinstance(axis, list):
        if len(axis) == 3:
            axis_scatter, axis_vert, axis_hor = axis
        else:
            raise ValueError("There must be 3 axes for 2-dimensional data")

    if data.ndim == 1:
        draw_func(data, axis=axis)
    elif data.shape[-1] == 2:
        draw_scatter(data, axis_scatter)
        draw_func(data, axis_vert, axis_hor)

    save_file(path_to_save)

    plt.show()
