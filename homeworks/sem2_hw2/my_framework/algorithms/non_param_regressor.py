import numpy as np
from .utils.distance import get_distances, Metric


class NonparametricRegressor():
    _k: int
    _X_train: np.ndarray
    _y_train: np.ndarray
    _metric: Metric

    def __init__(
        self,
        k: int = 1,
        metric: Metric = Metric.EUCLIDEAN
    ) -> None:

        if (k < 1 or not (isinstance(k, int))):
            raise ValueError(
                "k_neighbor must be int more than 0, "
                f"but given: {k}."
            )

        if (not (isinstance(metric, Metric))):
            raise ValueError(
                "metric must be Metric, "
                f"but given: {metric}"
            )

        self._k = k
        self._metric = metric

    def _get_weights(
        self,
        distances: np.ndarray
    ) -> np.ndarray:
        points_h = np.sort(distances)[:, self._k]
        points_h = points_h.reshape((distances.shape[0], 1))
        kernel_arguments = distances / points_h

        return (
            3/4 * (1 - kernel_arguments ** 2) *
            (np.absolute(kernel_arguments) <= 1)
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> None:
        if (X_train.shape[0] != y_train.shape[0]):
            raise ValueError("different dim")
        self._X_train = X_train.copy()
        self._y_train = y_train.copy()

    def predict(
        self,
        points: np.ndarray
    ) -> np.ndarray:

        if any([
            self._X_train is None,
            self._y_train is None
        ]):
            raise ValueError("X or y is empty")

        distances = get_distances(points, self._X_train, self._metric)
        weights = self._get_weights(distances)

        y = self._y_train.reshape((1, self._y_train.shape[0]))
        coefficients = np.sum(y * weights, axis=-1) / np.sum(weights, axis=-1)

        return coefficients
