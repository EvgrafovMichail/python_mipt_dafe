from materials.metrics import Metrics
import numpy as np
from Errors.Errors import (
    NoFitFoundError,
    ShapeMismatchError
)


class Nonparametric_regression():
    _points: np.ndarray
    _k: int
    _metric: str

    def __init__(self, k: int = 5, metric: str = "l1") -> None:
        if isinstance(k, int) and Metrics(metric):
            self._k = k
            self._points = None
            self._metric = metric
        else:
            if isinstance(k, int):
                raise TypeError(
                    'metric from Metric is requred',
                    f'got {metric} instead'
                )
            elif metric in Metrics:
                raise ValueError(
                    "Integer k is requred",
                    f'got {k} instead'
                )

    def fit(self, points: np.ndarray) -> None:
        if points.shape[0] == 0:
            raise ShapeMismatchError(
                "Points shape = 0"
            )
        self._points = points.copy()

    def predict(self, x_test: np.ndarray) -> np.ndarray:

        if self._points is None:
            raise NoFitFoundError("Predict was called before Fit")

        x_train, y_train = np.hsplit(self._points, 2)

        x_test_extended = np.tile(x_test, x_train.shape[0])

        distances = np.abs(x_test_extended - x_train.flatten())

        k_elem = np.sort(distances)[:, self._k]

        x_test = x_test.flatten()

        dist_for_width_window = np.abs(k_elem)
        dist_for_width_window = np.reshape(
            dist_for_width_window, (dist_for_width_window.shape[0], 1)
        )
        array_for_core = distances / dist_for_width_window

        W = self._core(array_for_core)

        upper_part = y_train.flatten() * W
        upper_part = np.sum(upper_part, 1)

        bottom_part = np.sum(W, 1)

        y_predicted = upper_part / bottom_part

        return y_predicted

    def _core(self, points: np.ndarray):
        weight = 0.75*(1-points**2) * (np.abs(points) <= 1)
        return weight
