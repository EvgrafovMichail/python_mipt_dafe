import typing
from typing import Any, Callable
import matplotlib
from matplotlib import pyplot as plt
import numpy as np



def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any] = max
) -> np.ndarray:
    
    if not (isinstance(data, np.ndarray)):
        raise ValueError("data must be a np.ndarray")
    
    if len(data.shape) == 1:
        data = data.reshape(data.shape[0], 1)


    key = np.vectorize(key)
    sort_data = key(data.copy())

    q1 = np.array(sort_data[int(sort_data.size * 0.25)])
    q3 = np.array(sort_data[int(sort_data.size * 0.75)])

    E = (q3 - q1) * 1.5
    lower_border = np.where(data >= q1 - E, 1, 0)
    lower_border = np.where(np.sum(lower_border, axis=1) != lower_border.shape[1], 0, 1)
    upper_border = np.where(data <= q3 + E, 1, 0)
    upper_border = np.where(np.sum(upper_border, axis=1) != lower_border.shape[1], 0, 1)
    result = np.where(lower_border + upper_border == 2, 1, 0)
    return np.argwhere(result == 1)[:, 0]
