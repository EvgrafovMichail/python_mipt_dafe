from typing import Union, Callable, Any
import numpy as np

from utils.models import OutliersSettings


def Core(x):
    return 3/4 * (1 - x ** 2) * (abs(x) <= 1)


class NR:
    _dist_index: int
    _metric: str
    _fit: bool
    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]

    def __init__(self, dist_index: int, metric: str = 'l2') -> None:
        if metric != 'l1' and metric != 'l2':
            raise TypeError("Invalid metric")
        if dist_index < 0:
            raise ValueError("Invalid Distance index")
        self._metric = metric
        self._dist_index = dist_index

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray) -> None:
        if abscissa.shape[0] != ordinates.shape[0]:
            raise RuntimeError("Not enough abscissa or ordinates")

        self._abscissa = np.transpose(np.atleast_2d(abscissa))  # сразу в правильном виде
        self._ordinates = ordinates
        self._fit = True

    def predict(self, abscissa):
        abscissa = np.transpose(np.atleast_2d(abscissa))    # привожу к правильному виду

        # наверно проще сделать одну проверку за весь код ради красоты, вместо else
        if self._metric == "l1":
            distances = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis=2, ord=1)
        if self._metric == "l2":
            distances = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis=2, ord=None)

        win_width = np.sort(distances).T[self._dist_index]
        weights = Core(distances / win_width)

        return np.sum(self._ordinates * weights, axis=1) / np.sum(weights, axis=1)


class KNN:
    _k_neighbours: int
    _metric: str
    _fit: bool
    _points: Union[np.ndarray, None]
    _labels: Union[np.ndarray, None]

    def __init__(self, k_neighbours, metric) -> None:
        if metric != 'l1' and metric != 'l2':
            raise ValueError("Invalid metric")
        if k_neighbours < 1:
            raise ValueError("Invalid number of neighbours")
        self._metric = metric
        self._k_neighbours = k_neighbours

    def fit(self, points, labels):
        self._points = points
        self._labels = labels
        self._fit = True

    def predict(self, points):
        if not self._fit:
            raise RuntimeError("Fit the data")

        # попытался сделать как в регрессии, через транспоны, не вышло
        a = np.repeat(self._points[np.newaxis, :, :], points.shape[0], axis=0)
        b = np.repeat(points[:, np.newaxis, :], self._points.shape[0], axis=1)

        # наверно проще сделать одну проверку за весь код ради красоты, вместо else
        if self._metric == 'l1':
            distances = np.linalg.norm(a-b, axis=2, ord=1)
        if self._metric == 'l2':
            distances = np.linalg.norm(a-b, axis=2, ord=None)

        np.sort(distances)

        win_width = np.transpose(np.atleast_2d(distances.T))[self._k_neighbours]
        arrCore = np.vectorize(Core)
        weights = arrCore(distances / win_width)[::, 0:self._k_neighbours]
        colors = self._labels[np.argsort(distances)][::, 0:self._k_neighbours]
        # colors имеет 1 и 0 в зависимости от цвета точки, -0.5 делает их либо с +, либо с -
        return np.where(np.sum((colors - 0.5) * weights, axis=1) > 0, 1, 0)


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
    settings: OutliersSettings = OutliersSettings(),
) -> np.ndarray:
    index_sorted = np.argsort(np.apply_along_axis(key, -1, data))
    data_sorted = np.sort(np.apply_along_axis(key, -1, data))

    q1 = data_sorted[int(data.shape[0] * settings._low_border)]
    q3 = data_sorted[int(data.shape[0] * settings._high_border)]
    e = (q3 - q1) * settings._epsilon

    return np.sort(index_sorted[np.add(data_sorted < q1 - e, data_sorted > q3 + e)])
