import numpy as np


from typing import Iterable, Union
from numbers import Real


class CallingOrder(Exception):
    pass


class RegressorABC():
    _metric: str
    _abscissa_train: Union[np.ndarray, None]
    _values: Union[np.ndarray, None]
    _k_neighbours: int
    _distances: np.ndarray

    def fit(self, abscissa: Iterable, ordinates: Iterable, k: int, metric: str = 'l2') -> None:
        ...

    def predict(
        self, abscissa: Union[Real, Iterable]
    ) -> np.ndarray:
        ...
    # ядро Епанечникова
    kernel = np.vectorize(lambda x: float((0.75 * (1-(x ** 2)))) if (abs(x) <= 1) else float(0))

    def _dist(self, points: Union[Real, Iterable]) -> np.ndarray:
        metics = ["l1", "l2"]

        points = np.array(points)
        if self._metric == metics[1]:  # евклидова метрика
            new_training_points = self._abscissa_train[np.newaxis, :]
            points = points[:, np.newaxis, :]
            distances = (  # расстояния от точек points до точек обучающей выборки
                            np.round((np.sum((points - new_training_points)**2, axis=2))**0.5, 10)
                            )
        if self._metric == metics[0]:  # манхэттенская метрика
            new_training_points = self._abscissa_train[np.newaxis, :]
            points = points[:, np.newaxis, :]
            distances = np.sum(np.abs(points - new_training_points), axis=-1)
        return distances
