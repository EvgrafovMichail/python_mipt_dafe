"""Non parametric regressor.
This module contain implementation of class NonParametricRegressor.

Examples:
    >>> import numpy as np
    >>> from solidipy_mipt import mse, mae, dc
    >>> from solidipy_mipt.algorithms import NonParametricRegressor
    >>> X = np.array([[1], [3], [5], [7]])
    >>> y = X * 2 + 1
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, train_ratio=0.6, shuffle=True)
    >>> np_regressor = NonParametricRegressor()
    >>> np_regressor.fit(X_train, y_train)
    >>> prediction = np_regressor.predict(X_test)
    >>> print(
    ...    f"{mse(prediction, y_test)=}\n"
    ...    f"{mae(prediction, y_test)=}\n"
    ...    f"{dc(prediction, y_test)=}"
    ... )
"""

import numpy as np

from ._predictor_abc import PredictorABC
from .utils.distance import get_distances, Metric
from ..utils.validate import check_size
from ..utils.errors import UntrainedModelError


class NonparametricRegressor(PredictorABC):
    """
    Nonparametric Regressor implementation.

    This class implements the NPRegressor algorithm.

    Parameters:
        k_neighbor: Neighbor number for adaptive window width calculation.
            Defaults to 1.

        metric: Metric for calculating distance.
        To see metric options, check solidipy_mipt.algorithms.distance.Metric.
            Defaults to Metric.EUCLIDEAN.

    Methods:
        fit(X_train, y_train): Train the NPRregressor with the provided training data.
        predict(X_test): Predict targets for test data using the trained NPRegressor.

    Raises:
        ValueError: If `k_neighbor` is not more than 0 or not int.
    """

    _k_neighbour: int
    _X_train: np.ndarray | None
    _y_train: np.ndarray | None

    def __init__(
        self,
        k_neighbor: int = 1,
        metric: Metric = Metric.EUCLIDEAN
    ) -> None:
        k_neighbor = int(k_neighbor)
        metric = Metric(metric)

        if k_neighbor < 1:
            raise ValueError(
                "k_neighbor must be int more than 0, "
                f"but given: {k_neighbor}."
            )

        self._k_neighbor = k_neighbor
        self._metric = metric

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> None:
        """
        Train the NPRegressor with the provided training data.

        Args:
            X_train: The training sample.
            y_train: Targets for given training sample.

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
        points: np.ndarray
    ) -> np.ndarray:
        """
        Predict targets for test data using the trained NPRegressor.

        Args:
            X_test: The test sample.

        Returns:
            prediction: Predicted targets for given test sample.

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

        check_size(points, self._X_train, axis=(-1, ))

        distances = get_distances(points, self._X_train, self._metric)
        weights = self._get_weights(distances)

        y = self._y_train.reshape((1, self._y_train.shape[0]))
        coefficients = np.sum(y * weights, axis=-1) / np.sum(weights, axis=-1)

        return coefficients

    def _get_weights(
        self,
        distances: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate weights for given `X_test` use Epanechnikov kernel.

        Args:
            distances: Distances between `X_test` and `X_train` samples.

        Return:
            weights: Calculated weights.
        """

        points_h = np.sort(distances)[:, self._k_neighbor].reshape((distances.shape[0], 1))

        kernel_arguments = distances / points_h
        weights = 3/4 * (1 - kernel_arguments ** 2) * (np.absolute(kernel_arguments) <= 1)

        return weights
