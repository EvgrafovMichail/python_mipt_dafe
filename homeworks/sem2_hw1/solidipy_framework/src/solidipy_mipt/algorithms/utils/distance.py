"""Common operations with distance between two points.

This module ...

Example:
    from solidipy.examples import distance

    
    if __name__ == "__main__":
        distance.start()
"""

import numpy as np

from enum import Enum
from ...utils.validate import check_size


class Metric(Enum):
    """
    Metric.
    """

    EUCLIDEAN = 1
    MANHATTAN = 2


def get_distances(
        points_1: np.ndarray,
        points_2: np.ndarray,
        metric=Metric.EUCLIDEAN
) -> np.ndarray: 
    """
    Get distances matrix between each two points from arrays with given metric.

    Args:
        points_1:
        points_2:
        metric:
    
    Return:
        distances:
    """

    check_size(points_1, points_2, axis=(-1, ), min_shapes_count=2)

    point_col = points_1.reshape(points_1.shape[0], 1, points_1.shape[1])
    point_row = points_2.reshape(1, points_2.shape[0], points_2.shape[1])

    match metric:
        case Metric.EUCLIDEAN:
            return np.sum((point_row - point_col) ** 2, axis=2)
        
        case Metric.MANHATTAN:
            return np.sum(np.abs(point_row - point_col), axis=2)
