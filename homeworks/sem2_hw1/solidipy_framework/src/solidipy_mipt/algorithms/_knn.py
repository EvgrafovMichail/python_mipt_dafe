"""K near neighbours.

This module ...

Example:
    from solidipy.examples import knn

    
    if __name__ == "__main__":
        knn.start()
"""

import numpy as np
import scipy.stats as sps

from .utils.distance import get_distances, Metric
from ._predictor_abc import PredicatorABC
from ..utils.validate import check_size


class KNN(PredicatorABC):
    """
    KNN.

    Args:
        k_neighbours: 
        k_neighbour:
        metric:
    """

    _k_neighbours: int
    _points: np.ndarray | None
    _targets: np.ndarray | None
    
    def __init__(
        self,
        k_neighbours: int = 5,
        k_neighbour: int = 1,
        metric: Metric = Metric.EUCLIDEAN
    ) -> None:
        k_neighbours = int(k_neighbours)
        metric = Metric(metric)

        if k_neighbours < 1:
            raise ValueError("bad k_neighbours") # TODO bad message
        
        self._k_neighbours = k_neighbours
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

        # TODO split to smaller methods

        if (not all([
            self._points is not None,
            self._targets is not None
        ])):
            raise ValueError() # TODO add custom error
        
        check_size(points, self._points, axis=(-1, ))
        
        distances = get_distances(points, self._points, self._metric)
        sorted_distances = np.sort(distances)
        points_h = sorted_distances[:, self._k_neighbour].reshape((distances.shape[0], 1))
        
        k_near_neighbours_indeces = np.argsort(distances)[:, :self._k_neighbours]
        k_near_neighbours_distances = sorted_distances[:, :self._k_neighbours]

        k_near_neighbours_labels = self._targets[k_near_neighbours_indeces]

        kernel_arguments = k_near_neighbours_distances / points_h
        weights = 3/4 * (1 - kernel_arguments ** 2) * (np.absolute(kernel_arguments) <= 1)

        k_near_neighbours_labels_with_weights = np.concatenate(
            (
                k_near_neighbours_labels,
                weights
            ),
            axis=1
        )

        weighted_mode = np.apply_along_axis(
            lambda x: np.bincount(
                x[:self._k_neighbours].astype(int),
                weights=x[self._k_neighbours:]
            ).argmax(),
            arr=k_near_neighbours_labels_with_weights,
            axis=1
        )

        return weighted_mode
