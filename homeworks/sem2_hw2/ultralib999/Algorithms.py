import numpy as np
from ultralib999.dev_only.Helpers import _could_be_compared
from ultralib999.GlobalVars import DistanceMetrics
from typing import Any, Callable


class NPR:
    _supported_metrics = [DistanceMetrics.MANHATTAN, DistanceMetrics.CLASSIC]

    def __init__(self, metric: str = DistanceMetrics.CLASSIC) -> None:
        if metric not in self._supported_metrics:
            raise TypeError(f"wrong metric, "
                            f"supported metrics are {self._supported_metrics}")
        self._metric = metric
        self._k = None
        self._axis_x = None
        self._axis_y = None

    # i-я строка - расстояния от всех векторов из a до i-го вектора из b
    @staticmethod
    def _get_distances(a: np.ndarray, b: np.ndarray, metric_val: int) -> np.ndarray:
        _could_be_compared(a, b)

        _x = np.tile(a.T, a.shape[0]).T
        _y = np.repeat(b, repeats=a.shape[0], axis=0)
        return np.linalg.norm(_x - _y, axis=1, ord=metric_val)

    @staticmethod
    def _get_arrayed_kernel(u):
        tmp = 3 / 4 * (1 - u ** 2)
        return tmp if tmp <= 1 else 0

    def change_metric(self, metric: str):
        if metric not in self._supported_metrics:
            raise TypeError(f"wrong metric, "
                            f"supported metrics are {self._supported_metrics}")
        self._metric = metric

    def fit(self, axis_x: np.ndarray, axis_y: np.ndarray, k: int) -> None:
        _could_be_compared(axis_x, axis_y)
        if k > axis_y.shape[0]:
            raise ValueError("k is too big")
        self._axis_x = axis_x
        self._axis_y = axis_y
        self._k = k

    def predict(self, predict_from: np.ndarray) -> np.ndarray:
        if self._axis_x is None or self._axis_y is None or self._k is None:
            raise RuntimeError("NPR must fit before predict")
        if not isinstance(predict_from, np.ndarray):
            raise TypeError(
                f"Expected type numpy.ndarray, got: {type(predict_from)}"
            )
        if self._metric not in self._supported_metrics:
            raise TypeError(f"wrong metric, "
                            f"supported metrics are {self._supported_metrics}")
        # у нас же x это не всегда точка ;(
        # это всё портит
        if len(predict_from.shape) == 1:
            predict_from = predict_from.reshape(predict_from.shape[0], 1)
            self._axis_x = self._axis_x.reshape(self._axis_x.shape[0], 1)

        distances = (self._get_distances(
            self._axis_x, predict_from,
            1 if self._metric == DistanceMetrics.MANHATTAN else 2
        ).reshape(
            (predict_from.shape[0], predict_from.shape[0])
        ))

        h_windows = np.sort(distances, axis=1)[
            (
                    (np.arange(distances.size) - self._k) %
                    (distances.shape[1]) == 0
            ).reshape(distances.shape)].reshape(-1, 1)

        h_windows = np.repeat(h_windows, repeats=distances.shape[0], axis=1)

        top = (self._axis_y * np.vectorize(
            lambda p, h: self._get_arrayed_kernel(p / h)
        )(distances, h_windows)).sum(axis=1)

        bottom = (np.vectorize(
            lambda p, h: self._get_arrayed_kernel(p / h)
        )(distances, h_windows)).sum(axis=1)

        res = top / bottom
        return res


class KNN:
    _supported_metrics = [DistanceMetrics.MANHATTAN, DistanceMetrics.CLASSIC]

    def __init__(
            self, win_index=4, neighbours: int = 4,
            metric: str = DistanceMetrics.MANHATTAN
    ) -> None:
        if metric not in self._supported_metrics:
            raise TypeError(f"wrong metric, supported metrics are {self._supported_metrics}")

        if not isinstance(neighbours, int):
            raise TypeError("neighbours must be integer")
        if neighbours <= 0:
            raise ValueError("neighbours must be greater than zero")

        if not isinstance(win_index, int):
            raise TypeError("win_size must be integer")
        if win_index <= 0:
            raise ValueError("win_size must be greater than zero")

        self._metric = metric
        self._neighbours_amount = neighbours
        self._win_index = win_index
        self._axis_x = None
        self._axis_y = None

    def change_metric(self, metric: str):
        if metric not in self._supported_metrics:
            raise TypeError(f"wrong metric, "
                            f"supported metrics are {self._supported_metrics}")
        self._metric = metric

    def fit(self, axis_x: np.ndarray, axis_y: np.ndarray) -> None:
        _could_be_compared(axis_x, axis_y)
        self._axis_x = axis_x
        self._axis_y = axis_y

    def predict(self, predict_from: np.ndarray) -> np.ndarray:
        if self._axis_x is None or self._axis_y is None:
            raise RuntimeError("KNN must fit before predict")
        if not isinstance(predict_from, np.ndarray):
            raise TypeError(f"Expected type numpy.ndarray, got: {type(predict_from)}")
        if self._metric not in self._supported_metrics:
            raise TypeError(f"wrong metric, supported metrics are {self._supported_metrics}")

        if len(predict_from.shape) == 1:
            predict_from = predict_from.reshape(predict_from.shape[0], 1)
            self._axis_x = self._axis_x.reshape(self._axis_x.shape[0], 1)
        distances = np.linalg.norm(
            self._axis_x - predict_from[:, np.newaxis],
            axis=2, ord=1 if self._metric == DistanceMetrics.MANHATTAN else 2
        )

        h_windows = np.sort(distances).T[self._win_index]

        kernels = np.where(
            np.abs(np.sort(distances).T / h_windows).T <= 1,
            3 / 4 * (1 - (np.sort(distances).T / h_windows).T ** 2
                     ), 0
        )[::, :self._neighbours_amount]
        closest_points = self._axis_y[np.argsort(distances)][::, :self._neighbours_amount]

        return np.where(((closest_points != self._axis_y[0]) * kernels).sum(axis=1) >= 0.5, 1, 0)


# новое
def get_boxplot_outliers(
        data: np.ndarray,
        key: Callable[[Any], Any],
) -> np.ndarray:
    """
    Функция для поиска выбросов
    :param data: значения, среди которых будет идти поиск
    :param key: тип сортировки
    :returns: индексы выбросов в data
    :raises ValueError:
    """
    if not (isinstance(data, np.ndarray)):
        raise ValueError("data must be a np.ndarray")
    if len(data.shape) == 1:
        data = data.reshape(data.shape[0], 1)

    keys = ["quicksort", "mergesort", "heapsort", "stable"]
    if not (key in keys):
        raise ValueError(f"Unexpected key {key}, supported keys are: {keys}")

    data += 2 * abs(data.min())  # мега крутой трюк жееееееееесть

    data_dist = np.apply_along_axis(lambda arr: np.sum(arr * arr), axis=1, arr=data)
    data_dist = data_dist.reshape(len(data_dist), 1)
    sorted_data = np.argsort(data_dist, kind=key, axis=0)

    quart_first = sorted_data[int(data.shape[0] * 0.25)]
    quart_third = sorted_data[int(data.shape[0] * 0.75)]

    epsilon = ((data_dist[quart_third] - data_dist[quart_first]) * 1.5)[0]

    left_extra = np.argwhere(data_dist < (data_dist[quart_first] - epsilon))
    right_extra = np.argwhere(data_dist > (data_dist[quart_third] + epsilon))

    if left_extra.size == 0:
        return right_extra
    if right_extra.size == 0:
        return left_extra
    return np.hstack((left_extra, right_extra))
