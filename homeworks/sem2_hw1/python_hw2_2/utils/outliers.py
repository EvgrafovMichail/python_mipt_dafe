import numpy as np
from typing import Any, Callable
a = np.array([[1, -2, 1], [1, 1, 1], [12, 3, 3]])
b = np.array([0, 1, 1])
# print(np.where(a[2] > b))
# print(np.where(np.sum(a, axis=1) != a.shape[1], 0, 1))


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
) -> np.ndarray:
    if not isinstance(data, np.ndarray):
        raise TypeError("there is not np.ndarray")

    if len(data.shape) == 1:  # нам в любом случае нужен двумерный массив координат
        data = data.reshape(data.shape[0], 1)
    sort_data = key(data.copy(), axis=0)
    # print("sort data:", sort_data, "\n")
    qwart1 = np.array(sort_data[int(sort_data.shape[0] * 0.25)][0])
    # print("sort data:", qwart1, "\n")
    qwart3 = np.array(sort_data[int(sort_data.shape[0] * 0.75)][0])
    # print("sort data:", qwart3, "\n")
    tunnel = (qwart3 - qwart1) * 1.5
    mask1 = np.where(data >= qwart1 - tunnel, 1, 0)
    # print(mask1)
    mask1 = np.where(np.sum(mask1, axis=1) // 1 != 1, 0, 1)
    print("mask1:", mask1, "\n")
    mask2 = np.where(data <= qwart3 + tunnel, 1, 0)
    # print(mask2)
    mask2 = np.where(np.sum(mask2, axis=1) // 1 != 1, 0, 1)
    # print("mask2:", mask2, "\n")
    ans_mask = np.where(mask1 + mask2 == 2, 1, 0)
    # print("ans data:", ans_mask, "\n")
    return np.where(ans_mask == 1, 0, 1)
