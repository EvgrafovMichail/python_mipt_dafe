"""Non parametric regressor.

This module ...

Example:
    from solidipy.examples import np_regressor

    
    if __name__ == "__main__":
        np_regressor.start()
"""

import numpy as np

from ._predictor_abc import PredicatorABC
from .utils.distance import get_distances, Metric
from ..utils.validate import check_size


class NonparametricRegressor(PredicatorABC):
    """
    Non parametric regressor.

    Args:
        k_neighbour: 
        metric: 
    """

    _k_neighbour: int
    _points: np.ndarray | None
    _targets: np.ndarray | None

    def __init__(
        self,
        k_neighbour: int = 1,
        metric: Metric = Metric.EUCLIDEAN
    ) -> None:
        k_neighbour = int(k_neighbour)
        metric = Metric(metric)

        if k_neighbour < 1:
            raise ValueError("bad k_neighbours") # TODO bad message
        
        self._k_neighbour = k_neighbour
        self._metric = metric
    
    def fit(
        self, 
        points: np.ndarray,
        targets: np.ndarray
    ) -> None:
        """
        Fit.

        Args:
            points:
            targets:
        """

        check_size(points, targets)
        
        self._points = points.copy()
        self._targets = targets.copy()

    def predict(
        self, 
        points: np.ndarray
    ) -> np.ndarray:
        """
        Predict.

        Args:
            points:
        
        Returns:
            prediction: 
        """

        if (not all([
            self._points is not None,
            self._targets is not None
        ])):
            raise ValueError() # TODO add custom error
        
        check_size(points, self._points, axis=(-1, ))

        distances = get_distances(self._points, points, self._metric)
        
        points_h = np.sort(distances)[:, self._k_neighbour].reshape((distances.shape[0], 1))

        kernel_arguments = distances / points_h
        weights = 3/4 * (1 - kernel_arguments) * (np.absolute(kernel_arguments) <= 1)

        targets = self._targets.reshape((self._targets.shape[0], 1))
        coefficients = np.sum(targets * weights, axis=0) / np.sum(weights, axis=0)

        return coefficients
