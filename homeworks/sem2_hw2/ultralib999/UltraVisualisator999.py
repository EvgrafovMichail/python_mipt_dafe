from collections.abc import Iterable
import numpy as np
import matplotlib.pyplot as plt
from ultralib999.dev_only.Helpers import _default_vis_check, _draw_by_type, _save_pic, _check_dims
from ultralib999.GlobalVars import DiagramTypes


def visualize_distribution(
        axis: plt.Axes or list[plt.Axes],
        data: np.ndarray,
        diagram_type: str,
        path_to_save: str = ""
) -> None:
    """
    Функция визуализации распределения данных.

    :param axis: - ось, либо список осей.
    :param data: - численное описание данных (n-мерные точки), строка этой матрицы = точка.
    :param diagram_type: - Доступны 3 варианта диаграмм: violin, hist, boxplot.
    :param path_to_save: - путь к файлу, в который необходимо сохранить полученную картинку.
        Если путь к файлу - пустая строка, не сохранять картинку.
        Если файл с указанным именем существует, возбуждается warning и сохраняется картинка.
    :return: None
    :raises ValueError, ShapeMismatchError, TypeError:
    """
    # я так почитал, по pep287 рекомендуеца +- так писать докстринги

    # храним оси в list, но можем получить и как одну ось (пихнем в list потом)
    _default_vis_check(axis, path_to_save, enable_lists=True)
    if isinstance(axis, plt.Axes):
        axis = [axis, ]

    if not isinstance(data, np.ndarray):
        raise TypeError(f"data must be np.ndarray, got: {type(data)}")
    if not DiagramTypes.contains(diagram_type):
        raise ValueError(f"diagram_type must be one of {DiagramTypes}")

    # check dims
    if len(data.shape) == 1:
        data = data.reshape(data.shape[0], 1)
    dimensions = data.shape[1]

    # draw
    if dimensions != 2:
        for i in range(len(axis)):
            axis_single = axis[i]
            _draw_by_type(axis_single, diagram_type, data, value=i + 1)
    else:
        axis_scatter, axis_hist_vert, axis_hist_hor = axis

        axis_scatter.scatter(
            data.T[0],
            data.T[1],
            color="cornflowerblue",
            alpha=0.5
        )
        _draw_by_type(axis_hist_hor, diagram_type, data.T[0], True, 2)
        _draw_by_type(axis_hist_vert, diagram_type, data.T[1], False, 1)

        axis_hist_vert.invert_xaxis()
        axis_hist_hor.invert_yaxis()

    _save_pic(path_to_save)


def visualize_classification(
        axis: plt.Axes,
        points: np.ndarray,
        labels: np.ndarray,
        colors: list[str],
        path_to_save: str = ""
) -> None:
    """
    Функция визуализации классификации данных.

    :param axis: - одна ось.
    :param points: - численное описание данных (2-мерные точки), строка этой матрицы = точка.
    :param labels: - класс i-ой точки, все точки - одномерные.
    :param colors: - список цветов для классов, зацикливается при нехватке цветов,
        лишние цвета обрезаются.
    :param path_to_save: - путь к файлу, в который необходимо сохранить полученную картинку.
        Если путь к файлу - пустая строка, не сохранять картинку.
        Если файл с указанным именем существует, возбуждается warning и сохраняется картинка.
    :return: None
    :raises ShapeMismatchError, TypeError:
    """
    _default_vis_check(axis, path_to_save)

    _check_dims(points, 2, "points")  # двумерный не надо вытягивать
    labels = _check_dims(labels, 1, "labels")

    if not isinstance(colors, Iterable):
        raise TypeError("colors must be iterable")
    if any(not isinstance(el, str) for el in colors):
        raise TypeError("colors values must be string")

    # рисуэмо
    iter_clr = iter(colors)
    for label_unique in np.unique(labels):
        try:
            curr_clr = next(iter_clr)
        except StopIteration:
            iter_clr = iter(colors)
            curr_clr = next(iter_clr)
        axis.scatter(
            points.T[0][labels.T[0] == label_unique.T],
            points.T[1][labels.T[0] == label_unique.T],
            color=str(curr_clr),
            alpha=0.5
        )

    _save_pic(path_to_save)


def visualize_regression(
        axis: plt.Axes,
        abscissa: np.ndarray,
        ord_predicted: np.ndarray,
        err_corridors: np.ndarray = None,
        main_clr: str = "red",
        err_clr: str = "black",
        fill_clr: str = "orange",
        path_to_save: str = ""
) -> None:
    """
    Функция визуализации регрессии данных.

    :param axis: - одна ось.
    :param abscissa: - np.ndarray одномерный массив - ось x.
    :param ord_predicted: - np.ndarray одномерный массив предсказанных значений - ось у.
    :param err_corridors: - np.ndarray два одномерных массива,
        один - верхняя граница, второй - нижняя.
    :param main_clr err_clr fill_clr: - цвета на графике.
    :param path_to_save: - путь к файлу, в который необходимо сохранить полученную картинку.
        Если путь к файлу - пустая строка, не сохранять картинку.
        Если файл с указанным именем существует, возбуждается warning и сохраняется картинка.
        :return: None
    :raises ShapeMismatchError, TypeError:
    """
    _default_vis_check(axis, path_to_save)

    abscissa = _check_dims(abscissa, 1, "abscissa")
    ord_predicted = _check_dims(ord_predicted, 1, "ord_predicted")
    if err_corridors is not None:
        _check_dims(err_corridors[0], 1, "err_corridors[0]")
        _check_dims(err_corridors[1], 1, "err_corridors[1]")
    if any(not isinstance(i, str) for i in (main_clr, err_clr, fill_clr)):
        raise TypeError(f"err_clr and main_clr must be string, got: "
                        f"err_clr={type(err_clr)} and main_clr={type(main_clr)}")

    # рисуем
    axis.plot(abscissa, ord_predicted, color=main_clr)
    axis.plot(abscissa, err_corridors[0], linestyle="--", color=err_clr)
    axis.plot(abscissa, err_corridors[1], linestyle="--", color=err_clr)
    axis.fill_between(
        abscissa.T[0],
        err_corridors[0],
        err_corridors[1],
        color=fill_clr,
        alpha=0.5
    )

    _save_pic(path_to_save)
