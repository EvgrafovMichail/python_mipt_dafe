import matplotlib.pyplot as plt
import numpy as np

from typing import Union

FIGSIZE = (16, 9)


def visualize_1d_nonparam_regres(
        abscissa: np.ndarray[float],
        ordinates: np.ndarray[float],
        linspace: np.ndarray[float],
        predicts: np.ndarray[float],
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

    axis.legend()

    if path_to_save:
        figure.savefig(path_to_save, bbox_inches="tight")


def visualizate_2d_weighted_KNN(
        features: np.ndarray,
        targets: np.ndarray,
        path_to_save: Union[str, None]
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
        axis.scatter(abscissa[mask], ordinates[mask], label=f'class {number + 1}', alpha=0.5)

    axis.legend()

    if path_to_save:
        figure.savefig(path_to_save, bbox_inches="tight")
