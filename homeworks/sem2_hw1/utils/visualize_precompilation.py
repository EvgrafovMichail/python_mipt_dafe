import matplotlib.pyplot as plt
import numpy as np
from typing import Any
import os
from enum import Enum
import warnings


class Graphs(Enum):
    HIST = 'hist'
    VIOLIN = 'violin'
    BOXPLOT = 'boxplot'


def violin(data: np.ndarray, axis: plt.Axes) -> None:
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


def visualize_distribution(
    axis: list[plt.Axes],
    data: np.ndarray,
    diagram_type: Any,
    path_to_save: str = "",
) -> None:
    if diagram_type not in [graph.value for graph in Graphs]:
        raise ValueError(f"{diagram_type} is not a valid diagram type")

    if data.ndim == 1:
        if diagram_type == Graphs.HIST.value:
            axis[0].hist(
                data,
                color="cornflowerblue",
                edgecolor="blue",
                density=True
            )

        elif diagram_type == Graphs.BOXPLOT.value:
            axis[0].boxplot(
                data,
                boxprops=dict(color="lightsteelblue"),
                medianprops=dict(color="k"),
            )
            axis[0].set_yticks([])

        elif diagram_type == Graphs.VIOLIN.value:
            violin(data, axis[0])

    elif data.ndim == 2 and data.shape[1] == 2:
        abscissa, ordinates = data[:, 0], data[:, 1]
        axis[0].scatter(abscissa, ordinates, color="cornflowerblue", alpha=0.5)
        axis[1].hist(
            abscissa,
            bins=50,
            color="cornflowerblue",
            density=True,
            alpha=0.5,
        )
        axis[2].hist(
            ordinates,
            bins=50,
            color="cornflowerblue",
            orientation="horizontal",
            density=True,
            alpha=0.5,
        )
        axis[2].invert_yaxis()
        axis[1].invert_xaxis()

    else:
        raise ValueError("Data must be 1D or 2D with a secondary dimension of size 2")

    if path_to_save:
        if os.path.isfile(path_to_save):
            warnings.warn("File already exists at the specified path, overwriting it.")
        plt.savefig(path_to_save)
    plt.show()
