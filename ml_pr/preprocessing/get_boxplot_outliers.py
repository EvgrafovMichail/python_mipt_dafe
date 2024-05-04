from typing import Any, Callable
import numpy as np


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
) -> np.ndarray:

    if not (isinstance(data, np.ndarray)):
        raise ValueError("data must be a np.ndarray")

    if len(data.shape) == 1:
        data = data.reshape(data.shape[0], 1)
    elif data.ndim != 2:
        raise ValueError("Invalid dimension \
                         for computing outliers")

    index_sorted = np.argsort(np.apply_along_axis(key, -1, data))
    data_sorted = np.sort(np.apply_along_axis(key, -1, data))
    q1 = data_sorted[int(data.shape[0] * 0.25)]
    q3 = data_sorted[int(data.shape[0] * 0.75)]
    e = (q3 - q1) * 1.5

    return np.sort(index_sorted[np.logical_and(data_sorted < q1 - e,
                   data_sorted > q3 + e)])
