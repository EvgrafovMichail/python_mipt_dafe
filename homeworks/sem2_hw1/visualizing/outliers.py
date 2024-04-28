import matplotlib.pyplot as plt
from typing import (
    Callable,
    Any
)
import numpy as np


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
) -> np.ndarray:
    data_sorted = key(data) # вообще не поняла

    size = data_sorted.size
    q1 = data_sorted[int(size * 0.25)]
    q3 = data_sorted[int(size * 0.75)]

    e = (q3 - q1) * 1.5

    data_less = data_sorted <= q1 - e
    data_bigger = data_sorted >= q3 + e

    data_not_in_qs = data_bigger + data_less

    return np.argwhere(data_not_in_qs == True)[:, 0]

"""a = np.array([1, 3, 3, 4, 5, 6, 4, 8])
print(get_boxplot_outliers(a))"""