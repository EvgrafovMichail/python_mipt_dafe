import numpy as np
from .utils.distance import get_distances, Metric


class Wknn():
    _k: int
    _X_train: np.ndarray
    _y_train: np.ndarray

    def __init__(
        self,
        k: int = 5,
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

        sorted_distances = np.sort(distances)

        h = sorted_distances[:, self._k].reshape((distances.shape[0], 1))
        neighbor_distances = sorted_distances[:, :self._k]

        kernel_arguments = neighbor_distances / h
        weights = (
            3/4 * (1 - kernel_arguments ** 2) *
            (np.absolute(kernel_arguments) <= 1)
        )

        k_near_neighbor_indeces = np.argsort(distances)[:, :self._k]
        k_near_neighbor_labels = self._y_train[k_near_neighbor_indeces]
        k_near_neighbor_labels_with_weights = np.concatenate(
            (
                k_near_neighbor_labels,
                weights
            ),
            axis=1
        )

        weighted_mode = np.apply_along_axis(
            lambda x: np.bincount(
                x[:self._k].astype(int),
                weights=x[self._k:]
            ).argmax(),
            arr=k_near_neighbor_labels_with_weights,
            axis=1
        )

        return weighted_mode
