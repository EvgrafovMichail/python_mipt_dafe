import numpy as np
from typing import Union
from metrics.metric import Metric


class ShapeMismatchError(Exception):
    pass


class KNN:
    _metric: callable
    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]
    _width: float = 0
    _neighbours: int = 1

    def _kernel(self, u: np.ndarray) -> float:
        mask = abs(u) <= 1
        res = np.zeros(u.shape)
        res[mask] = 3 / 4 * (1 - u[mask] ** 2)

        return res

    def predict(self, x: np.ndarray) -> np.ndarray:

        if self._abscissa is None:
            raise RuntimeError("Np_regression wasn't fit")

        h = np.sort(self._metric(x, self._abscissa))[:, self._width]

        K = self._kernel(self._metric(x, self._abscissa) / h.reshape(h.shape[0], 1))

        mask = np.argsort(K, axis=-1)[:, ::-1]
        X = np.sort(K, axis=-1)[:, ::-1][:, :self._neighbours]
        lables = self._ordinates[mask][:, :self._neighbours]
        u = np.unique(self._ordinates)
        c = None
        for i in u:
            if c is None:
                c = np.sum(X * np.where(lables == i, 1, 0), axis=-1)
            else:
                c = np.append(c, np.sum(X * np.where(lables == i, 1, 0), axis=-1))
        c = c.reshape(u.shape[0], c.shape[0]//u.shape[0])
        return u[np.argmax(c, axis=0)]

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray) -> None:

        if abscissa.shape[0] != ordinates.shape[0]:
            raise ShapeMismatchError

        self._abscissa = abscissa
        self._ordinates = ordinates

    def __init__(self, metric: Metric = Metric.l2, k: int = 4, n: int = 1) -> None:

        if (k < 1):
            raise ValueError("k can't be < 1")

        if (n < 1):
            raise ValueError("n can't be < 1")

        self._neighbours = n
        self._width = k
        self._metric = metric
