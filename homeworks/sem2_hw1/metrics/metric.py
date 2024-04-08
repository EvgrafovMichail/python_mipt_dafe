import numpy as np
from enum import Enum


class ShapeMismatchError(Exception):
    pass


def l1(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a.copy()
    b = b.copy()

    if a.ndim == 1:
        a = a.reshape(a.shape[0], 1)
        b = b.reshape(b.shape[0], 1)

    a = a.reshape(a.shape[0], 1, a.shape[1])

    return np.sum(abs(a - b), axis=-1)


def l2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a.copy()
    b = b.copy()

    if a.ndim == 1:
        a = a.reshape(a.shape[0], 1)
        b = b.reshape(b.shape[0], 1)

    a = a.reshape(a.shape[0], 1, a.shape[1])

    return np.sum((a - b) ** 2, axis=-1)**0.5


class Metric(Enum):
    l1 = l1
    l2 = l2
