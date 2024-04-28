import numpy as np
from typing import Any, Callable


def get_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any] = None
) -> np.ndarray:
    if key:
        data_sorted = data[np.argsort(key(data))]
    else:
        data_sorted = data[data[:, 1].argsort()]
    q1 = data_sorted[round(data_sorted.shape[0] * 0.25)]
    q3 = data_sorted[round(data_sorted.shape[0] * 0.75)]
    e = (q3 - q1) * 1.5
    mask1 = np.prod(data < q1 - e, axis=1).astype(np.bool_)
    mask2 = np.prod(data > q3 + e, axis=1).astype(np.bool_)
    outliers = np.arange(0, data.shape[0])
    return outliers[mask1 + mask2]

# a = np.array([[-500,-500], [1,1], [2,2], [3,3], [4,4],
#               [50,50], [60,60],[70,7], [8,8], [900,900]])
# print(get_outliers(data=a))
