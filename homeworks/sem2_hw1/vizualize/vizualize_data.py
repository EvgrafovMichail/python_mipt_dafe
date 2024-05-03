import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
import os


class DiagramType(Enum):
    violin = 0,
    hist = 1,
    boxplot = 2


def _vizualize_violin(axis: plt.Axes, data: np.ndarray, vert=False) -> None:
    violin_parts = axis.violinplot(
        data,
        vert=vert,
        showmedians=True,
    )

    for body in violin_parts["bodies"]:
        body.set_facecolor("cornflowerblue")
        body.set_edgecolor("blue")
    for part in violin_parts:
        if part == "bodies":
            continue
        violin_parts[part].set_edgecolor("cornflowerblue")


def _vizualize_hist(axis: plt.Axes, data: np.ndarray, vert=False) -> None:
    axis.hist(
        data,
        bins=50,
        color="cornflowerblue",
        orientation="vertical" if not vert else "horizontal",
        density=True,
        alpha=0.5,
    )


def _visualize_boxplot(axis: plt.Axes, data: np.ndarray, vert=False) -> None:
    axis.boxplot(
        data,
        vert=vert,
        patch_artist=True,
        boxprops=dict(facecolor="lightsteelblue"),
        medianprops=dict(color="k"),
    )


def _visualise(axis: plt.Axes, data: np.ndarray, diagram_type: DiagramType, vert=False) -> None:
    if diagram_type == DiagramType.boxplot:
        _visualize_boxplot(axis, data, vert)
    elif diagram_type == DiagramType.hist:
        _vizualize_hist(axis, data, vert)
    elif diagram_type == DiagramType.violin:
        _vizualize_violin(axis, data, vert)
    else:
        raise RuntimeError('unknown diagram type')


def visualize_distribution(
    data: np.ndarray,
    diagram_type: DiagramType,
    path_to_save: str = "",
) -> None:
    if data.ndim == 1:
        figure = plt.figure(figsize=(8, 4))
        axis = figure.add_subplot()
        _visualise(axis, data, diagram_type)
        axis.set_yticks([])
    elif data.ndim == 2:
        figure = plt.figure(figsize=(8, 8))
        space = 0.2
        height = 3
        weight = 3

        grid = plt.GridSpec(height, weight, wspace=space, hspace=space)

        axis_scatter = figure.add_subplot(grid[:2, -2:])
        axis_scatter.scatter(data[:, 0], data[:, 1], color="cornflowerblue", alpha=0.5)

        axis_diagram_vertical = figure.add_subplot(grid[:2, 0], sharey=axis_scatter)
        axis_diagram_horizontal = figure.add_subplot(grid[-1, -2:], sharex=axis_scatter)

        _visualise(axis_diagram_vertical, data[:, 1], diagram_type, True)
        _visualise(axis_diagram_horizontal, data[:, 0], diagram_type)
        axis_diagram_vertical.invert_xaxis()
        axis_diagram_horizontal.invert_yaxis()

    if path_to_save != "":
        if os.path.exists(path_to_save + '.png'):
            print(f'Warning: the file {path_to_save} was overwritten')
        plt.savefig(path_to_save)


if __name__ == "__main__":
    path_to_save = './homeworks/sem2_hw1/images/kartinka'

    a = np.array([[1, 2], [5, 6], [9, 2], [1, 4]])
    b = np.array([1, 1, 3, 4, 5, 5, 6, 4, 5, 3, 7, 8])

    mean = [2, 3]
    cov = [[1, 1], [1, 2]]
    space = 0.2

    visualize_distribution(np.random.multivariate_normal(mean, cov, size=1000), DiagramType.boxplot, path_to_save)
