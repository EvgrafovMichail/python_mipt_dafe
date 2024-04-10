import numpy as np
from typing import Union
from metrics.metric import Metric


class ShapeMismatchError(Exception):
    pass


class NPR:
    _metric: callable
    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]
    _width: float = 0

    def _kernel(self, u: np.ndarray) -> float:
        mask = abs(u) <= 1
        res = np.zeros(u.shape)
        res[mask] = 3 / 4 * (1 - u[mask] ** 2)

        return res

    def predict(self, x: np.ndarray) -> np.ndarray:

        if self._abscissa is None:
            raise RuntimeError("Np_regression wasn't fit")

        h = np.sort(self._metric(x, self._abscissa), axis=-1)[:, self._width]

        K = self._kernel(self._metric(x, self._abscissa)/h.reshape(h.shape[0], 1))

        res = np.sum(self._ordinates.reshape(1, self._ordinates.shape[0])*K, axis=-1) / np.sum(K, axis=-1)

        return res

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray) -> None:

        if abscissa.shape[0] != ordinates.shape[0]:
            raise ShapeMismatchError

        self._abscissa = abscissa
        self._ordinates = ordinates

    def __init__(self, metric: Metric = Metric.l2, k: int = 4) -> None:

        if (k < 1):
            raise ValueError("k can't be < 1")

        self._width = k
        self._metric = metric
