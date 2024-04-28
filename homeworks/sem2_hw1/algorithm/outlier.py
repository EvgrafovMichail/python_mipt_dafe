import math
import numpy as np
from typing import Any, Callable


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
    path_to_save
) -> np.ndarray:
    # так понимаю key() сортирует массив,второй параметр сортировать по убыванию или по возрастанию
    data_sorted = key(data, False)
    q1 = (data_sorted[math.ceil(len(data_sorted) * 0.25)])
    q3 = (data_sorted[int(len(data_sorted) * 0.75)])
    epsilon = (q3 - q1) * 1.5
    trash = np.argwhere(np.any(((q1 - epsilon > data_sorted), (data_sorted > q3 + epsilon))))
    return trash
