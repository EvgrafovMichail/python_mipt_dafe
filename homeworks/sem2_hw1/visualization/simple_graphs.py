import matplotlib.pyplot as plt
import numpy as np

from algorithms.help_functions import set_violin


def draw_scatter(
    data: np.ndarray,
    axis: plt.Axes,
) -> None:
    abscissa, ordinates = data[::, 0], data[::, 1]
    axis.scatter(
        abscissa,
        ordinates,
        alpha=0.5,
        color="cornflowerblue",
    )


def draw_hist(
    data: np.ndarray,
    axis_hist_vert: plt.Axes = None,
    axis_hist_hor: plt.Axes = None,
    *,
    axis: plt.Axes = None
) -> None:
    if not (axis is None):
        axis.hist(
            data,
            color="cornflowerblue",
            density=True,
        )
    else:
        abscissa, ordinates = data[::, 0], data[::, 1]

        axis_hist_hor.hist(
            abscissa,
            bins=50,
            color="cornflowerblue",
            density=True,
            alpha=0.5,
        )
        axis_hist_vert.hist(
            ordinates,
            bins=50,
            color="cornflowerblue",
            orientation="horizontal",
            density=True,
            alpha=0.5,
        )

        axis_hist_hor.invert_yaxis()
        axis_hist_vert.invert_xaxis()


def draw_violin(
    data: np.ndarray,
    axis_hist_vert: plt.Axes = None,
    axis_hist_hor: plt.Axes = None,
    *,
    axis: plt.Axes = None
) -> None:
    if not (axis is None):
        violin_parts = axis.violinplot(
            data,
            vert=False,
            showmedians=True,
        )

        set_violin(violin_parts)

        axis.set_yticks([])
    else:
        abscissa, ordinates = data[::, 0], data[::, 1]

        violin_vert_parts = axis_hist_vert.violinplot(
            ordinates,
            vert=True,
            showmedians=True,
        )
        violin_hor_parts = axis_hist_hor.violinplot(
            abscissa,
            vert=False,
            showmedians=True,
        )

        set_violin(violin_vert_parts)
        set_violin(violin_hor_parts)


def draw_box(
    data: np.ndarray,
    axis_hist_vert: plt.Axes = None,
    axis_hist_hor: plt.Axes = None,
    *,
    axis: plt.Axes = None
) -> None:
    if not (axis is None):
        axis.boxplot(
            data,
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="lightsteelblue"),
            medianprops=dict(color="k"),
        )

        axis.set_yticks([])
    else:
        abscissa, ordinates = data[::, 0], data[::, 1]

        axis_hist_vert.boxplot(
            ordinates,
            patch_artist=True,
            vert=True,
            boxprops=dict(facecolor="lightsteelblue"),
            medianprops=dict(color="k"),
        )
        axis_hist_hor.boxplot(
            abscissa,
            patch_artist=True,
            vert=False,
            boxprops=dict(facecolor="lightsteelblue"),
            medianprops=dict(color="k"),
        )
