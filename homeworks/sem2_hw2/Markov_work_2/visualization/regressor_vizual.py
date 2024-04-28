import matplotlib.pyplot as plt
import numpy as np
import warnings
import os

FIGSIZE = (16, 9)


def visualize_results(
    axis: plt.Axes,
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    predictions: np.ndarray,
    error_corridor_ord: np.ndarray = None,
) -> None:
    ind = np.argsort(abscissa)

    axis.scatter(abscissa, ordinates, label='source', c='aqua', s=50)
    axis.scatter(abscissa, predictions, label='prediction', c='steelblue')
    if error_corridor_ord is not None:  # рисуем коридор ошибок, если он есть
        y_upper = ordinates[ind] + error_corridor_ord
        y_lower = ordinates[ind] - error_corridor_ord
        axis.fill_between(abscissa[ind], y_lower, y_upper, color='b', alpha=0.2)

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()


def visualize_comp(
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    predictions: np.ndarray,
    error_corridor_ord: np.ndarray,
    path_to_save: str = "",
) -> None:
    _, axis = plt.subplots(figsize=FIGSIZE)
    axis.set_title("nonparam_regres", fontsize=15, fontweight="bold", c="dimgray")
    axis.set_xlabel('abscissa', fontsize=15, fontweight="bold", c="dimgray")
    axis.set_ylabel('ordinates', fontsize=15, fontweight="bold", c="dimgray")
    visualize_results(axis,
                      abscissa,
                      ordinates,
                      predictions,
                      error_corridor_ord)

    if str != "":  # сохраняем изображение
        if os.path.exists(path_to_save):
            warnings.warn("Warning a file with the specified name exists")
        plt.savefig(path_to_save)
