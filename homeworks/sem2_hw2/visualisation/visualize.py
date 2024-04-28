import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
from materials.diagrams import diagrams
import warnings
from itertools import cycle
from enum import Enum
from Errors.Errors import ShapeMismatchError
from os import path

FIGSIZE = (16, 9)


class Colors(Enum):
    BLACK = "black"
    WHITE = "white"


def visualize_regression(
    full_data: np.ndarray,
    trend: np.ndarray,
    error_corridor: Optional[tuple[np.ndarray, np.ndarray]] = None,
    path_to_save: Optional[str] = ""
) -> None:

    if not isinstance(full_data, np.ndarray):
        raise TypeError(
            "np.ndarray type is intended for full_data"
        )
    if not isinstance(trend, np.ndarray):
        raise TypeError(
            "np.ndarray type is intended for trend"
        )

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    ax1.set_title("Full data", fontsize=15, fontweight="bold", c="dimgray")
    ax2.set_title("Trend :3", fontsize=15, fontweight="bold", c="dimgray")

    _visualize_regression_additional(full_data, ax1)
    _visualize_regression_additional(trend, ax2, trendy=True)

    if error_corridor:
        if (
            not isinstance(error_corridor[0], np.ndarray)
            or
            not isinstance(error_corridor[1], np.ndarray)
        ):
            raise TypeError(
                "np.ndarray type is intended for error_corridor containments"
            )
        _visualize_regression_additional(error_corridor[1], ax2, True)
        _visualize_regression_additional(error_corridor[0], ax2, True)

    save = _saving_mechanism(path_to_save)
    if save:
        plt.savefig(path_to_save)

    plt.show()


def visualize_classification(
    points: np.ndarray,
    labels: np.ndarray,
    colors: Optional[list[Colors]] = None,
    axis: Optional[plt.Axes] = None,
    path_to_save: str = ""
) -> None:

    if colors is None:
        colors = list(Colors)

    if axis and not isinstance(axis, plt.Axes):
        raise TypeError(
            "Unknown type for axis"
        )
    if not isinstance(points, np.ndarray):
        raise TypeError(
            "np.ndarray type is intended for points"
        )
    if not isinstance(labels, np.ndarray):
        raise TypeError(
            "np.ndarray type is intended for labels"
        )
    if labels.shape[0] != points.shape[0] or labels.shape[0] == 0:
        raise ShapeMismatchError(
            f"Features shape {points.shape[0]} != targets shape {labels.shape[0]}",
            "or it has a shape = 0"
        )

    colors_cycle = cycle([color for color in colors])
    labels_unique = np.unique(labels)

    if axis is None:
        _, axis = plt.subplots(figsize=FIGSIZE)

    for label in labels_unique:
        label_mask = labels == label
        axis.scatter(*points[label_mask].T, color=next(colors_cycle))

    save = _saving_mechanism(path_to_save)

    if save:
        plt.savefig(path_to_save)
    axis.grid(True)

    plt.show()


def visualize_distribution(
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: diagrams,
    path_to_save: str = "",
) -> None:
    if not isinstance(data, np.ndarray):
        raise TypeError(
            "np.ndarray type is intended for data"
        )
    if not diagrams(diagram_type):
        raise ValueError(
            "Unknown diagram_type"
        )

    save = _saving_mechanism(path_to_save)

    if data.shape[1] == 2:
        if not isinstance(axis, list):
            raise TypeError(
                "Axis is strictly a list of axis in order: main, left, down"
            )
        if len(axis) != 3:
            raise ShapeMismatchError(
                f"Axis should have a length of 3, got {len(axis)} instead"
            )
        for ax in axis:
            if not isinstance(ax, plt.Axes):
                raise TypeError(
                    "Axis is strictly a list of axis in order: main, left, down"
                )
        _visualize_three_diagrams(
            np.hsplit(data, 2)[0], np.hsplit(data, 2)[1],
            diagram_type, axis, save, path_to_save
        )

    if data.shape[1] == 1:
        _visualize_one_diagram(
            data, diagram_type, axis, save, path_to_save
        )


def _visualize_three_diagrams(
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    diagram_type: diagrams,
    axis: list[plt.Axes, plt.Axes, plt.Axes],
    save: bool = False,
    path_to_save: str = ""
) -> None:

    axis_scatter = axis[0]
    axis_vert = axis[1]
    axis_hor = axis[2]
    axis_scatter.scatter(abscissa, ordinates, color="cornflowerblue", alpha=0.5)

    if diagrams.hist == diagram_type:
        _make_two_hists(axis_hor, axis_vert, abscissa, ordinates)

    if diagrams.violin == diagram_type:
        _make_two_violins(axis_hor, axis_vert, abscissa, ordinates)

    if diagrams.boxplot == diagram_type:
        _make_two_boxplot(axis_hor, axis_vert, abscissa, ordinates)

    if save:
        plt.savefig(path_to_save)

    plt.show()


def _visualize_one_diagram(
    data: np.ndarray,
    diagram_type,
    axis: plt.Axes,
    save: bool = False,
    path_to_save: str = ""
) -> None:
    if not isinstance(axis, plt.Axes):
        raise TypeError(
            "Unknown type for axis"
        )

    if diagrams.hist == diagram_type:
        axis.hist(
            data,
            bins=50,
            color="cornflowerblue",
            density=True,
            alpha=0.5,
        )

    if diagrams.violin == diagram_type:
        violin_parts = axis.violinplot(
            data,
            vert=False,
            showmedians=True,
        )

        for body in violin_parts["bodies"]:
            body.set_facecolor("cornflowerblue")
            body.set_edgecolor("blue")

        for part in violin_parts:
            if part == "bodies":
                continue
            violin_parts[part].set_edgecolor("cornflowerblue")

        axis.set_yticks([])

    if diagrams.boxplot == diagram_type:
        axis.boxplot(
            data,
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="lightsteelblue"),
            medianprops=dict(color="k"),
        )
    if save:
        plt.savefig(path_to_save, format='png', dpi=1200)

    plt.show()


def _visualize_regression_additional(
    points: np.ndarray,
    axis: Optional[plt.Axes] = None,
    ticky: Optional[bool] = False,
    trendy: Optional[bool] = False
) -> None:

    if ticky:
        axis.plot(*points.T, color="blue", linestyle="dotted")
    if trendy:
        axis.plot(*points.T, color="blue")
    elif not trendy and not ticky:
        axis.scatter(*points.T)
    axis.grid(True)


def _saving_mechanism(path_to_save: str = "") -> bool:
    save = True

    if not isinstance(path_to_save, str):
        raise TypeError(
            "path_to_save has to be str type"
        )

    if path_to_save != "":
        if path.exists(path_to_save):
            warnings.warn(
                f"File {path_to_save} already exists, hope it's nothing important :)",
                Warning
            )
    else:
        save = False

    return save


def _make_beautiful(violin_parts_hor, violin_parts_vert):
    for body in violin_parts_hor["bodies"]:
        body.set_facecolor("cornflowerblue")
        body.set_edgecolor("blue")

    for part in violin_parts_hor:
        if part == "bodies":
            continue
        violin_parts_hor[part].set_edgecolor("cornflowerblue")

    for body in violin_parts_vert["bodies"]:
        body.set_facecolor("cornflowerblue")
        body.set_edgecolor("blue")

    for part in violin_parts_vert:
        if part == "bodies":
            continue
        violin_parts_vert[part].set_edgecolor("cornflowerblue")


def _make_two_hists(axis_hor, axis_vert, abscissa, ordinates):
    axis_hor.hist(
        abscissa,
        bins=50,
        density=True,
        alpha=0.5,
    )
    axis_vert.hist(
        ordinates,
        bins=50,
        orientation="horizontal",
        density=True,
        alpha=0.5,
    )


def _make_two_violins(axis_hor, axis_vert, abscissa, ordinates):
    violin_parts_hor = axis_hor.violinplot(
        abscissa,
        vert=False,
        showmedians=True,
    )
    violin_parts_vert = axis_vert.violinplot(
        ordinates,
        vert=True,
        showmedians=True,
    )
    _make_beautiful(violin_parts_hor, violin_parts_vert)

    axis_hor.set_yticks([])
    axis_vert.set_yticks([])


def _make_two_boxplot(axis_hor, axis_vert, abscissa, ordinates):
    axis_hor.boxplot(
        abscissa,
        vert=False,
        patch_artist=True,
        boxprops=dict(facecolor="lightsteelblue"),
        medianprops=dict(color="k"),
    )
    axis_vert.boxplot(
        ordinates,
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor="lightsteelblue"),
        medianprops=dict(color="k"),
    )
