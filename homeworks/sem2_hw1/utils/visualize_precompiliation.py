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


def violin(data: np.ndarray, axis: plt.axes) -> None:
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
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: Any,
    path_to_save: str = "",
) -> None:
    # if (diagram_type not in Graphs.TYPE.value):
    #     raise ValueError('{diagram_type} не может быть аргументом')
    if (len(data.shape) == 1):
        if diagram_type == Graphs.HIST.value:
            axis.hist(
                data,
                color="cornflowerblue",
                edgecolor="blue",
            )

        elif diagram_type == Graphs.BOXPLOT.value:
            axis.boxplot(
                data,
                boxprops=dict(facecolor="lightsteelblue"),
                medianprops=dict(color="k"),
            )
            axis.set_yticks([])  # так как одномерный случай не нужен y
        elif diagram_type == Graphs.VIOLIN.value:
            violin(data, axis)
        else:
            raise ValueError(f'{diagram_type} не может быть аргументом')

    elif len(data.shape) == 2:
        # считаем что на вход приходит [axis]
        abscissa = data[:, 0]
        ordinates = data[:, 1]
        # cтроим главный график
        axis[0].scatter(abscissa, ordinates, color="cornflowerblue", alpha=0.5)
        # abcissa
        axis[1].hist(
            abscissa,
            bins=50,
            color="cornflowerblue",
            density=True,
            alpha=0.5,
        )
        # ordinate
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

    if len(path_to_save) != 0:
        if os.path.isfile(path_to_save):
            warnings.warn("В указанном пути есть файл, мы его заменили")
        plt.savefig(path_to_save)
    plt.show()
