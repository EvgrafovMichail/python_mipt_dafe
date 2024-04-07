from typing import Union
import numpy as np


def Core(x):
    return 0.75 * (1 - x**2) if abs(x) <= 1 else 0
# по непонятным причинам копипаст кода из регрессии перестаёт работать
# броадкаст (80,) на (80,320) не удаётся (хотя камон, просто скопируй это строчку 320 раз)


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
        if points.shape[0] != labels.shape[0]:
            raise ValueError("Wrong amount of input")
        self._points = points
        self._labels = labels
        self._fit = True

    def predict(self, points):
        if not self._fit:
            raise RuntimeError("Fit the data")
        # попытался сделать как в регрессии, через транспоны, не вышло
        a = np.repeat(self._points[np.newaxis, :, :], points.shape[0], axis=0)
        b = np.repeat(points[:, np.newaxis, :], self._points.shape[0], axis=1)
        if self._metric == 'l1':
            distances = np.linalg.norm(a-b, axis=2, ord=1)
        if self._metric == 'l2':
            distances = np.linalg.norm(a-b, axis=2, ord=None)

        # по непонятным причинам не даёт назвать её distances
        dists = np.sort(distances)
        win_width = np.transpose(np.atleast_2d(dists.T[self._k_neighbours]))
        arrCore = np.vectorize(Core)
        weights = arrCore(dists / win_width)[::, 0:self._k_neighbours]
        colors = self._labels[np.argsort(distances)][::, 0:self._k_neighbours]
        # colors имеет 1 и 0 в зависимости от цвета точки, -0.5 делает их либо с +, либо с -
        return np.where(np.sum((colors - 0.5) * weights, axis=1) > 0, 1, 0)
