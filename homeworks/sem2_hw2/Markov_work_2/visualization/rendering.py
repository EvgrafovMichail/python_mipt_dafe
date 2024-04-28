from matplotlib.axis import Axis
from typing import Callable, Union, Dict
import matplotlib.pyplot as plt
import numpy as np
import warnings
import os


types = dict()  # словарь с фунциями отрисовки для 2D случая


def add_to_types(func: Callable):  # декоратор для добавления нужных функций в словарь
    types[func.__name__] = func
    return func


def visualize_distribution(
    axis: Union[plt.Axes, Dict[str, plt.Axes]],
    data: np.ndarray,
    diagram_type: str,
    path_to_save: str = "",
) -> None:
    ''' для визуализации двумерного массива данных
        axis это словарь c ключами: "axis_vert", "axis_hor", "axis_scatter"'''
    if diagram_type not in types:
        raise ValueError("Uncorrect type of diagram")
    if len(data.shape) == 2:  # обрабатываем двумерный случай
        visualize_diagrams_2D(axis=axis,
                              abscissa=data[:, 0],
                              ordinates=data[:, 1],
                              diagram_type=diagram_type)
    elif len(data.shape) == 1:  # обрабатываем одномерный случай
        visualize_diagrams_1D(axis, data, diagram_type)
    else:
        raise ValueError

    if str != "":  # сохраняем изображение
        if os.path.exists(path_to_save):
            warnings.warn("Warning a file with the specified name exists")
        plt.savefig(path_to_save)


def visualize_diagrams_1D(
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: str
) -> None:
    '''визуализация для одномерного массива данных'''
    if diagram_type == "hist":
        axis.hist(
            data,
            bins=50,
            color="cornflowerblue",
            density=True,
            alpha=0.5,
        )
    if diagram_type == "boxplot":
        axis.boxplot(
            data,
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="aquamarine"),
            medianprops=dict(color="k"),
        )
    if diagram_type == "violin":
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


def visualize_diagrams_2D(
    axis: dict[plt.Axes],
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    diagram_type: str
) -> None:
    ''' визуализация для двумерного массива данных
        axis это словарь c ключами: "axis_vert", "axis_hor", "axis_scatter"'''

    axis["axis_scatter"].scatter(abscissa, ordinates, color="cornflowerblue", alpha=0.5)

    axis["axis_hor"], axis["axis_vert"] = types[diagram_type](axis["axis_hor"],
                                                              axis["axis_vert"],
                                                              abscissa,
                                                              ordinates)

    axis["axis_hor"].invert_yaxis()
    axis["axis_vert"].invert_xaxis()


@add_to_types
def hist(axis_hor: Axis, axis_vert: Axis, abscissa: np.ndarray, ordinates: np.ndarray) -> Axis:
    for i, k, l in zip([abscissa, ordinates], [axis_hor, axis_vert], ["vertical", "horizontal"]):
        k.hist(
            i,
            bins=50,
            color="cornflowerblue",
            density=True,
            alpha=0.5,
            orientation=l,
        )

    return axis_hor, axis_vert


@add_to_types
def boxplot(axis_hor: Axis, axis_vert: Axis, abscissa: np.ndarray, ordinates: np.ndarray) -> Axis:
    vertical = False

    for i, k in zip([abscissa, ordinates], [axis_hor, axis_vert]):
        k.boxplot(
            i,
            vert=vertical,
            patch_artist=True,
            boxprops=dict(facecolor="aquamarine"),
            medianprops=dict(color="k"),
        )
        k.set_yticks([])
        vertical = not vertical

    return axis_hor, axis_vert


@add_to_types
def violin(axis_hor: Axis, axis_vert: Axis, abscissa: np.ndarray, ordinates: np.ndarray) -> Axis:
    vertical = False

    for i, k in zip([abscissa, ordinates], [axis_hor, axis_vert]):
        violin_parts = k.violinplot(
            i,
            vert=vertical,
            showmedians=True,
            )
        for body in violin_parts["bodies"]:
            body.set_facecolor("violet")
            body.set_edgecolor("purple")

        for part in violin_parts:
            if part == "bodies":
                continue

            violin_parts[part].set_edgecolor("m")

        k.set_yticks([])
        vertical = not vertical

    return axis_hor, axis_vert
