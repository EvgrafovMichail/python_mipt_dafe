import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Callable, Optional
from itertools import cycle
from warnings import warn
from os.path import isdir, exists

from sci_fw.helpers.data import check_array, check_shapes
from sci_fw.enumerations import Plot_Type

DEFAULT_COLORS = ("royalblue", "darkorange")


def save_plot(
    path_to_save: str
) -> None:
    path_to_save = str(path_to_save)
    if not path_to_save:
        return
    if exists(path_to_save):
        if isdir(path_to_save):
            path_to_save += "figure.png"
        else:
            warn("Overwriting existing file while saving")
    plt.savefig(path_to_save)


def visualize_classification(
    axis: plt.Axes,
    features: np.ndarray,
    labels: np.ndarray,
    colors: Optional[list] = None
) -> None:
    features = check_array(features)
    labels = check_array(labels)
    check_shapes(features, labels)
    if colors is None:
        colors = list(DEFAULT_COLORS)
    colors = cycle(colors)

    unique_labes = np.unique(labels)
    for label in unique_labes:
        mask = labels == label
        axis.scatter(features[mask][:, 0], features[mask][:, 1], c=next(colors))


def visualize_regression(
    axis: plt.Axes,
    points: np.ndarray,
    prediction: np.ndarray,
    error: Optional[np.ndarray] = None
) -> None:
    points = check_array(points)
    if points.ndim == 1:
        points = points[:, np.newaxis]
    if points.ndim != 2 or points.shape[1] > 2:
        raise ValueError("Only 2d points can be visualized")
    prediction = check_array(prediction)
    if error is not None:
        error = check_array(error)
        check_shapes(prediction, error)

    axis.margins(x=0)

    axis.scatter(points[:, 0], points[:, 1], c=DEFAULT_COLORS[1], alpha=.5)
    plot_data_1d(axis, prediction, Plot_Type.LINE)
    if error is not None:
        bound = prediction
        bound[:, 1] += error
        plot_data_1d(axis, bound, Plot_Type.LINE, linestyle="--")
        bound[:, 1] -= 2 * error
        plot_data_1d(axis, bound, Plot_Type.LINE, linestyle="--")


def plot_data_1d(
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: Plot_Type,
    ** kwargs
) -> None:
    """
    Kwargs are forwarded to the plotting function
    """
    if not isinstance(axis, plt.Axes):
        raise ValueError("Axis is of an incorrect type")
    data = check_array(data)
    diagram_type = Plot_Type(diagram_type)

    if diagram_type == Plot_Type.HIST:
        kwargs.setdefault("edgecolor", DEFAULT_COLORS[0])
        kwargs.setdefault("alpha", .5)
        kwargs.setdefault("color", DEFAULT_COLORS[0])
        kwargs.setdefault("bins", 50)
        kwargs.setdefault("orientation", "vertical")
        axis.hist(data, **kwargs)
    elif diagram_type == Plot_Type.BOX:
        kwargs.setdefault("vert", False)
        kwargs.setdefault("patch_artist", True)
        kwargs.setdefault("boxprops", dict(facecolor=DEFAULT_COLORS[0]))
        kwargs.setdefault("medianprops", dict(color="k"))
        axis.boxplot(data, **kwargs)
    elif diagram_type == Plot_Type.LINE:
        kwargs.setdefault("color", DEFAULT_COLORS[0])
        axis.plot(data[:, 0], data[:, 1], **kwargs)
    elif diagram_type == Plot_Type.VIOLIN:
        kwargs.setdefault("vert", False)
        kwargs.setdefault("showmedians", True)
        axis.violinplot(data, **kwargs)


def visualize_distribution(
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: Any,
    path_to_save: str = "",
) -> None:
    """
    If 'data' is multidimensional, elements of 'axis' go in the following order:
        0) scatter 1) y distibution 2) x distribution
    Othervise data will be plotted on the first axis as usual
    """
    if isinstance(axis, plt.Axes):
        axis = np.array([axis])
    axis = check_array(axis)
    data = check_array(data)

    for ax in axis:
        ax.margins(x=0, y=0)

    if (data.ndim == 1) or (data.ndim == 2 and data.shape[1] == 1):
        plot_data_1d(axis[0], data, diagram_type)
    elif data.ndim == 2 and data.shape[1] == 2:
        if axis.size < 3:
            raise ValueError("Not enough axes to plot data")
        axis[0].scatter(data[:, 0], data[:, 1], color=DEFAULT_COLORS[0], alpha=0.5)
        kwargs = dict()
        plot_data_1d(axis[2], data[:, 0], diagram_type, **kwargs)
        if diagram_type == Plot_Type.HIST:
            kwargs.setdefault("orientation", "horizontal")
        elif diagram_type == Plot_Type.BOX:
            kwargs.setdefault("vert", True)
        elif diagram_type == Plot_Type.VIOLIN:
            kwargs.setdefault("vert", True)
        plot_data_1d(axis[1], data[:, 1], diagram_type, **kwargs)

    save_plot(path_to_save)


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
) -> np.ndarray:
    data = check_array(data)
    if data.ndim == 1:
        data = data[:, np.newaxis]
    elif data.ndim != 2:
        raise ValueError("Invalid dimension for computing outliers")

    size = data.shape[0]
    quartile_data = np.apply_along_axis(key, 1, data.T)
    first_quartile = quartile_data[:, int(size * .25)]
    third_quartile = quartile_data[:, int(size * .75)]
    epsilon = (third_quartile - first_quartile) * 1.5
    outliers_lower = (data < (first_quartile - epsilon)).any(axis=1)
    outliers_upper = (data > (third_quartile + epsilon)).any(axis=1)
    outliers = outliers_lower | outliers_upper
    return np.nonzero(outliers)
