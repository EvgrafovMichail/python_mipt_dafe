import matplotlib.pyplot as plt
import numpy as np
import warnings
import os
from utils.diagram_type import Diagram_type

plt.style.use("ggplot")
SPACE = 0.2


def visualize_distribution(
    data: np.ndarray,
    diagram_type: Diagram_type,
    path_to_save: str = "",
) -> None:
    if (len(data.shape) == 1):
        _, axis = plt.subplots(figsize=(16, 9))
        match(diagram_type):
            case Diagram_type.VIOLIN:
                axis.violinplot(
                    data,
                    vert=False,
                    showmedians=True,
                )
                axis.set_yticks([])
            case Diagram_type.HIST:
                axis.hist(
                    data,
                    bins=100,
                    color="cornflowerblue",
                    density=True,
                    alpha=0.5,
                )
            case Diagram_type.BOXPLOT:
                axis.boxplot(
                    data,
                    vert=False,
                    patch_artist=True,
                    boxprops=dict(facecolor="blue"),
                    medianprops=dict(color="k"),
                )
        _get_results(path_to_save=path_to_save)

    elif (len(data.shape) == 2 and data.shape[1] == 2):
        figure = plt.figure(figsize=(8, 8))
        grid = plt.GridSpec(4, 4, wspace=SPACE, hspace=SPACE)

        axis_scatter = figure.add_subplot(grid[:-1, 1:])
        axis_hist_vert = figure.add_subplot(
            grid[:-1, 0],
            sharey=axis_scatter,
        )
        axis_hist_hor = figure.add_subplot(
            grid[-1, 1:],
            sharex=axis_scatter,
        )

        abscissa, ordinates = data[:, 0], data[:, 1]
        axis_scatter.scatter(
            abscissa,
            ordinates,
            color="cornflowerblue",
            alpha=0.5
        )
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
        _get_results(path_to_save=path_to_save)


def _get_results(
    path_to_save: str = "",
) -> None:
    if (path_to_save == ""):
        plt.show()
    else:
        if os.path.exists(path_to_save):
            warnings.warn(
                f"the file at"
                f"'{os.path.abspath(path_to_save)}'"
                f"path already exists",
                DeprecationWarning
            )
        plt.savefig(path_to_save)


absc = np.random.normal(size=1000)
ordi = np.random.normal(size=1000)
data = np.column_stack([absc, ordi])

# data = np.random.normal(size=1000)
visualize_distribution(
    data=data,
    diagram_type=Diagram_type.HIST,
    path_to_save="TEST.png"
)
