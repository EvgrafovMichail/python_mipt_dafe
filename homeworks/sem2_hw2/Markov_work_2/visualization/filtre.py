import numpy as np
from typing import Callable, Any


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
) -> np.ndarray:
    '''фунция key сама заботится o том, какая размерность пространства'''
    # сортируем по key
    data_sorted = sorted(data, key=key)
    # Определяем 1 и 3 квартили
    q1 = data_sorted[int(len(data_sorted) * 0.25)]
    q3 = data_sorted[int(len(data_sorted) * 0.75)]
    e = (q3 - q1) * 1.5
    # вычисляем нужные индексы по маске
    mask = ((q1 - e) <= data) & (data <= (q3 + e))  # маска
    indexs = np.where(mask)[0]

    return indexs
