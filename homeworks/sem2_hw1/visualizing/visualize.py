from diagram_types import Diagram_types
import matplotlib.pyplot as plt
from typing import Any
import numpy as np
import warnings
import os


NROWS = 2
NCOLS = 2
SPACES = 0.2
H_RATIOS = (4, 1)
W_RATIOS = (1, 4)


def visualize_distribution(
    # axis: plt.Axes,немного не понятно, как привязать к двумерному
    figure: plt.Figure,
    data: np.ndarray,
    diagram_type: str,
    path_to_save: str = "",
) -> None:
    if not isinstance(figure, plt.Figure):
        raise TypeError("Figure expected to be plt.Figure")

    if not isinstance(data, np.ndarray):
        raise TypeError("Data expected to be np.ndarray")

    if not diagram_type in Diagram_types:
        raise(f"Unexpected diagram type: {diagram_type}")    

    if data.ndim == 1:
        axis = figure.add_subplot()
        _visualize_diagram(
            axis=axis,
            data=data,
            diagram_type=diagram_type
        )

    elif data.ndim == 2 and data.shape[1] == 2:
        _visualize(
            figure=figure,
            data=data,
            diagram_type=diagram_type
        )

    else:
        raise RuntimeError(
            f"Unexpected data dimensity: {data.ndim}"
        )


    if not path_to_save == "":
        _save_to_file(
            path_to_save=path_to_save
        )


def _visualize_diagram(
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: Any,
    orientation: Any = "vertical"
) -> None:
    if diagram_type == Diagram_types.HIST:
        axis.hist(
            data=data,
            orientation=orientation
        )

    if orientation == "vertical":
        orientation = 1
    else:
        orientation = 0

    if diagram_type == Diagram_types.VIOLIN:
        axis.violin(
            data=data,
            vert=orientation
        )

    if diagram_type == Diagram_types.BOXPLOT:
        axis.boxplot(
            data=data,
            vert=orientation
        )


def _visualize(
        figure: plt.Figure,
        data: np.ndarray,
        diagram_type: str
) -> None:
    grid = figure.add_gridspec(
            nrows=NROWS,
            ncols=NCOLS,
            width_ratios=W_RATIOS,
            height_ratios=H_RATIOS,
            wspace=SPACES,
            hspace=SPACES
        )

    abscissa = data[:, 0]
    ordinates = data[:, 1]

    axis = figure.add_subplot(grid[0, 1])
    axis_vertical = figure.add_subplot(grid[0, 0], sharey=axis)
    axis_horizontal = figure.add_subplot(grid[1, 1], sharex=axis)

    axis.scatter(abscissa, ordinates)

    _visualize_diagram(
        axis=axis_vertical,
        data=ordinates,
        diagram_type=diagram_type
    )

    _visualize_diagram(
        axis=axis_horizontal,
        data=abscissa,
        diagram_type=diagram_type,
        orientation="horizontal"
    )


def _save_to_file(
        path_to_save: str
) -> None:
    if os.path.exists(os.path.dirname(path_to_save)):
        warnings.warn("File was rewritten")

    plt.savefig(path_to_save)
