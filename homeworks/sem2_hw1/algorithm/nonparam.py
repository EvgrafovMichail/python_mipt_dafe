import numpy as np
from typing import Union
from metrics_distance import ShapeMismatchError
from metrics_distance import distance


class NREGR:
    _k_neighbours: int  # Количество соседей для учета
    _metric: str  # Метрика растояния l1 для манхэтенского расстояния или l2 для евклидова растояния
    _bool_test = False

    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]

    def __init__(self, k_neighbours: int, metric: str) -> None:
        if metric not in ['l1', 'l2']:
            raise ValueError(f"not correct metric {metric}")

        self._metric = metric

        if not isinstance(k_neighbours, int):
            raise TypeError(f'arguments {k_neighbours} must be have type int')

        self._k_neighbours = k_neighbours

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray) -> None:
        if abscissa.shape[0] != ordinates.shape[0]:
            raise ShapeMismatchError(f"shape {abscissa.shape[0]} != shape {ordinates.shape[0]}")

        if not isinstance(abscissa, np.ndarray) or not isinstance(ordinates, np.ndarray):
            raise TypeError(" must be have type nd.ndarray")

        self._abscissa = np.array(abscissa.copy())
        self._ordinates = np.array(ordinates.copy())
        self._bool_test = True  # Флаг, указывающий на наличие тестовых данных

    def predict(self, abscissa: np.ndarray):
        if not self._bool_test:
            raise ValueError("not test data")

        if not isinstance(abscissa, np.ndarray):
            raise TypeError("must be have type nd.ndarray")

        if len(abscissa.shape) == 1:
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(self._abscissa.shape[0], 1)
        # Вычисляем попарные расстояния между тестовыми и обучающими точками
        dist = distance(self._abscissa, abscissa, self._metric)
        # Вычисляем высоту окна
        wind_heigh = np.sort(dist, axis=-1)[:, self._k_neighbours]
        # Вычисляем функцию ядра для регрессии
        core = np.where(np.abs(dist / wind_heigh[:, np.newaxis]) <= 1,
                        0.75 * (1 - (dist / wind_heigh[:, np.newaxis]) ** 2), 0)
        # Возвращаем среднее взвешенное значение ординат
        return np.sum(self._ordinates * core, axis=1) / np.sum(core, axis=1)
