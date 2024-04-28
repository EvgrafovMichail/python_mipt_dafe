import numpy as np
import matplotlib.pyplot as plt
from typing import Optional

from utils.models import (
    DiagramType,
    HistogramSettings,
    BoxplotSettings,
    ViolinSettings,
    MegahistSettings,
)


def plot_hist(
    axis: plt.Axes,
    data: np.ndarray,
    settings: Optional[HistogramSettings] = HistogramSettings(),
) -> None:
    axis.hist(
        data,
        bins=settings._bins,
        color=settings._color,
        edgecolor=settings._edgecolor,
        density=settings._density,
        alpha=settings._alpha,
        orientation=settings._orientation,
    )


def plot_boxplot(
    axis: plt.Axes,
    data: np.ndarray,
    settings: Optional[BoxplotSettings] = BoxplotSettings(),
) -> None:
    axis.boxplot(
        data,
        vert=settings._vert,
        boxprops=settings._boxprops,
        medianprops=settings._medianprops,
    )


def plot_violin(
    axis: list[plt.Axes],
    data: np.ndarray,
    settings: Optional[ViolinSettings] = ViolinSettings(),
) -> None:
    violin_parts = axis.violinplot(
        data,
        vert=settings._vert,
        showmedians=settings._showmedians,
    )

    for body in violin_parts["bodies"]:
        body.set_facecolor(settings._facecolor)
        body.set_edgecolor(settings._edgecolor)

    for part in violin_parts:
        if part == "bodies":
            continue

        violin_parts[part].set_edgecolor(settings._othercolor)


def plot_megahist(
    axis: list[plt.Axes],
    data: np.ndarray,
    diagram_type: DiagramType,
    settings: Optional[MegahistSettings],
) -> None:
    abscissa = data[::, 0]
    ordinates = data[::, 1]

    axis_scatter, axis_hist_hor, axis_hist_vert = axis

    axis_scatter.scatter(
        abscissa,
        ordinates,
        color=settings._color,
        alpha=settings._alpha
        )

    vert_settings = settings._settings
    match DiagramType(diagram_type):
        case DiagramType.HIST:
            plot_hist(axis=axis_hist_vert, data=abscissa, settings=vert_settings)
            hor_settings = vert_settings
            hor_settings._orientation = "horizontal"
            plot_hist(axis=axis_hist_hor, data=ordinates, settings=hor_settings)

        case DiagramType.BOXPLOT:
            plot_boxplot(axis=axis_hist_vert, data=abscissa, settings=vert_settings)
            hor_settings = vert_settings
            hor_settings._vert = True
            plot_boxplot(axis=axis_hist_hor, data=ordinates, settings=hor_settings)

        case DiagramType.VIOLIN:
            plot_violin(axis=axis_hist_vert, data=abscissa, settings=vert_settings)
            hor_settings = vert_settings
            hor_settings._vert = True
            plot_violin(axis=axis_hist_hor, data=abscissa, settings=hor_settings)

        case _:
            raise RuntimeError

    axis_hist_hor.invert_yaxis()
    axis_hist_vert.invert_xaxis()
