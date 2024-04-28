import matplotlib.pyplot as plt
import numpy as np
import warnings
import os.path

from typing import Union

FIGSIZE = (16, 9)


def visualize_1d_nonparam_regres(
        abscissa: np.ndarray[float],
        ordinates: np.ndarray[float],
        linspace: np.ndarray[float],
        predicts: np.ndarray[float],
        approximation_min: np.ndarray[float] = None,
        approximation_max: np.ndarray[float] = None,
        path_to_save: Union[str, None] = None
) -> None:
    figure, axis = plt.subplots(figsize=FIGSIZE)
    axis.set_title("Nonparametric Regressor", fontsize=17, fontweight="bold", c="dimgray")
    axis.axis((np.min(abscissa),
               np.max(abscissa),
               np.min(ordinates) - (np.max(ordinates) - np.min(ordinates)) / 10,
               np.max(ordinates) + (np.max(ordinates) - np.min(ordinates)) / 10
               ))
    axis.grid(True)

    axis.scatter(abscissa, ordinates, c="royalblue", label="input data", alpha=0.5)
    axis.plot(linspace, predicts, c="blue", label="approximation")
    if approximation_min is not None and approximation_max is not None:
        axis.plot(linspace, approximation_min, linestyle="--", c="royalblue", alpha=0.5)
        axis.plot(
            linspace,
            approximation_max,
            linestyle="--",
            c="royalblue",
            alpha=0.5,
            label="σ-coridor",
        )

    axis.legend()

    if path_to_save:
        figure.savefig(path_to_save, bbox_inches="tight")


def visualizate_2d_weighted_KNN(
        features: np.ndarray,
        targets: np.ndarray,
        path_to_save: Union[str, None],
        color: np.ndarray = None,
) -> None:
    figure, axis = plt.subplots(figsize=FIGSIZE)
    axis.set_title("Weighted KNN", fontsize=17, fontweight="bold", c="dimgray")
    abscissa, ordinates = np.hsplit(features, 2)
    axis.axis((np.min(abscissa) - (np.max(abscissa) - np.min(abscissa)) / 10,
               np.max(abscissa) + (np.max(abscissa) - np.min(abscissa)) / 10,
               np.min(ordinates) - (np.max(ordinates) - np.min(ordinates)) / 10,
               np.max(ordinates) + (np.max(ordinates) - np.min(ordinates)) / 10
               ))
    axis.grid(True)

    for number, target_type in enumerate(np.unique(targets)):
        mask = targets == target_type
        if color is None:
            axis.scatter(abscissa[mask], ordinates[mask], label=f'class {number + 1}', alpha=0.5)
        else:
            axis.scatter(
                abscissa[mask],
                ordinates[mask],
                c=color[number % color.shape[0]],
                label=f'class {number + 1}',
                alpha=0.5,
            )

    axis.legend()

    if path_to_save:
        figure.savefig(path_to_save, bbox_inches="tight")


def visualize_distribution(
    figure: plt.Figure,
    data: np.ndarray,
    diagram_type: str,
    path_to_save: str = None,
) -> None:
    if diagram_type not in ("violin", "hist", "boxplot"):
        raise ValueError(f"Incorrect diagram type {diagram_type}")

    if diagram_type == "violin":
        axis = figure.add_subplot()
        axis.set_title("Distribution Violin", fontsize=17, fontweight="bold", c="dimgray")
        axis.violinplot(data, vert=False, showmedians=True)

    elif diagram_type == "hist":
        if data.ndim == 1:
            axis = figure.add_subplot()
            axis.set_title("Distribution Hist", fontsize=17, fontweight="bold", c="dimgray")
            axis.hist(data, bins=50, color="cornflowerblue")
        elif data.ndim == 2 and data.shape[1] == 2:
            space = 0.2

            abscissa = data[:, 0]
            ordinates = data[:, 1]

            grid = plt.GridSpec(4, 4, wspace=space, hspace=space)

            axis_scatter = figure.add_subplot(grid[:-1, 1:])
            axis_hist_vert = figure.add_subplot(
                grid[:-1, 0],
                sharey=axis_scatter,
            )
            axis_hist_hor = figure.add_subplot(
                grid[-1, 1:],
                sharex=axis_scatter,
            )

            axis_scatter.scatter(abscissa, ordinates, color="cornflowerblue", alpha=0.5)
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
        else:
            raise ValueError("The function can draw max 2D hist")

    elif diagram_type == "boxplot":
        axis = figure.add_subplot()
        axis.set_title("Distribution Boxplot", fontsize=17, fontweight="bold", c="dimgray")
        axis.boxplot(data, vert=False)

    if path_to_save is not None:
        if os.path.isfile(path_to_save):
            warnings.warn("A file with that name already exists")
        figure.savefig(path_to_save, bbox_inches="tight")
