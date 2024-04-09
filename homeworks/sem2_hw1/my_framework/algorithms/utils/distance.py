import numpy as np
from enum import Enum


class Metric(Enum):

    EUCLIDEAN = 1
    MANHATTAN = 2


def get_distances(
        first: np.ndarray,
        second: np.ndarray,
        metric=Metric.EUCLIDEAN
) -> np.ndarray:

    col = first.reshape(first.shape[0], 1, first.shape[1])
    row = second.reshape(1, second.shape[0], second.shape[1])

    if (metric == Metric.EUCLIDEAN):
        return np.sum((row - col) ** 2, axis=2)

    elif (metric == Metric.MANHATTAN):
        return np.sum(np.abs(row - col), axis=2)

    else:
        raise ValueError("different dim")
