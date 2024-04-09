"""Weighted k-nearest neighbors.
This module contain implementation of class WKNN(Weighted K-Nearest Neighbors).

Examples:
    >>> import numpy as np
    >>> from solidipy_mipt import accuracy
    >>> from solidipy_mipt.algorithms import WKNN
    >>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    >>> y = np.array([0, 1, 0, 1])
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, train_ratio=0.6, shuffle=True)
    >>> wknn = WKNN()
    >>> wknn.fit(X_train, y_train)
    >>> prediction = wknn.predict(X_test)
    >>> print(accuracy(prediction, y_test))
"""

import numpy as np

from .utils.distance import get_distances, Metric
from ._predictor_abc import PredictorABC
from ..utils.validate import check_size
from ..utils.errors import UntrainedModelError


class WKNN(PredictorABC):
    """
    Weighted k-Nearest Neighbors (WKNN) classifier implementation.

    This class implements the KNN algorithm for classification.

    Parameters:
        k_neighbors: Number of neighbors to consider for classification.
            Defaults to 5.

        metric: Metric for calculating distance.
        To see metric options, check solidipy_mipt.algorithms.distance.Metric.
            Defaults to Metric.EUCLIDEAN.

    Methods:
        fit(X_train, y_train): Train the WKNN classifier with the provided training data.
        predict(X_test): Predict labels for test data using the trained WKNN classifier.

    Raises:
        ValueError: If `k_neighbors` is not more than 0 or not int.
    """

    _k_neighbors: int
    _X_train: np.ndarray | None
    _y_train: np.ndarray | None
    _metric: Metric

    def __init__(
        self,
        k_neighbors: int = 5,
        metric: Metric = Metric.EUCLIDEAN
    ) -> None:
        k_neighbors = int(k_neighbors)
        metric = Metric(metric)

        if k_neighbors < 1:
            raise ValueError(
                "k_neighbors must be int more than 0, "
                f"but given: {k_neighbors}."
            )

        self._k_neighbors = k_neighbors
        self._metric = metric

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> None:
        """
        Train the WKNN classifier with the provided training data.

        Args:
            X_train: The training sample.
            y_train: Target labels for given training sample.

        Returns:
            None

        Raises:
            ShapeMismatchError: If `X_train` and `y_train` shapes mismatch.
        """

        check_size(X_train, y_train)

        self._X_train = X_train.copy()
        self._y_train = y_train.copy()

    def predict(
        self,
        X_test: np.ndarray
    ) -> np.ndarray:
        """
        Predict labels for test data using the trained WKNN classifier.

        Args:
            X_test: The test sample.

        Returns:
            prediction: Predicted labels for given test sample.

        Raises:
            ShapeMismatchError: If `X_train` and `X_test` shapes mismatch.
            UntrainedModelError: If use untrained model.
        """

        if not all([
            self._X_train is not None,
            self._y_train is not None
        ]):
            raise UntrainedModelError(
                "",
                self.__class__.__name__
            )

        check_size(X_test, self._X_train, axis=(-1, ))

        distances = get_distances(X_test, self._X_train, self._metric)
        weights = self._get_weights(distances)
        k_near_neighbor_labels = self._get_k_near_neighbor_labels(distances)

        k_near_neighbor_labels_with_weights = np.concatenate(
            (
                k_near_neighbor_labels,
                weights
            ),
            axis=1
        )

        return self._get_weighted_mode(k_near_neighbor_labels_with_weights)

    def _get_weights(
        self,
        distances: np.ndarray
    ) -> np.ndarray:
        """
        Calculate weights for given `X_test` use Epanechnikov kernel.

        Args:
            distances: Distances between `X_test` and `X_train` samples.

        Return:
            weights: Calculated weights.
        """

        sorted_distances = np.sort(distances)

        points_h = sorted_distances[:, self._k_neighbors].reshape((distances.shape[0], 1))
        k_near_neighbor_distances = sorted_distances[:, :self._k_neighbors]

        kernel_arguments = k_near_neighbor_distances / points_h
        weights = 3/4 * (1 - kernel_arguments ** 2) * (np.absolute(kernel_arguments) <= 1)

        return weights

    def _get_k_near_neighbor_labels(
        self,
        distances: np.ndarray
    ) -> np.ndarray:
        """
        It returns k-near neighbor labels for given `X_test`.

        Args:
            distances: Distances between `X_test` and `X_train` samples.

        Returns:
            k_near_neighbor_labels: K-near neighbor labels for given `X_test`.
        """

        k_near_neighbor_indeces = np.argsort(distances)[:, :self._k_neighbors]
        k_near_neighbor_labels = self._y_train[k_near_neighbor_indeces]

        return k_near_neighbor_labels

    def _get_weighted_mode(
        self,
        k_near_neighbor_labels_with_weights: np.ndarray
    ) -> np.ndarray:
        """
        Calculate weighted mode for given k-near neighbor labels concatenated with their weights.
        Weighted modes will be calculated for all `X_test` not for 1 point.

        Args:
            k_near_neighbor_labels_with_weights: K-near neighbor labels which
            concatenated with their weights.

        Returns:
            weighted_mode: Weighted mode for given k-near neighbor labels which
            concatenated with their weights.
        """

        weighted_mode = np.apply_along_axis(
            lambda x: np.bincount(
                x[:self._k_neighbors].astype(int),
                weights=x[self._k_neighbors:]
            ).argmax(),
            arr=k_near_neighbor_labels_with_weights,
            axis=1
        )

        return weighted_mode
