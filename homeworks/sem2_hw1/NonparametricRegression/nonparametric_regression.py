from typing import Union
import numpy as np


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
