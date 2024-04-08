import numpy as np


def _could_be_compared(x: np.ndarray, y: np.ndarray) -> None:
    if not (isinstance(x, np.ndarray) and isinstance(y, np.ndarray)):
        raise ValueError(f"Expected numpy.ndarray, got: {type(x)}, {type(y)}")
    if x.shape[0] != y.shape[0] and y.size != 0:
        raise IndexError(f"two arrays must have the same "
                         f"non-zero length, got: {x.shape[0]} {y.shape[0]}")
