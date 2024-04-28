import numpy as np
from typing import Union
from metrics_distance import ShapeMismatchError, distance


class KNN:
    _k_neighbours: int  # Количество соседей для учета
    _metric: str  # Метрика растояния l1 для манхэтенского расстояния или l2 для евклидова растояния
    _abscissa: Union[np.ndarray, None]
    _labels: Union[np.ndarray, None]
    _bool_test = False

    def __init__(self, k_neighbours: int, metric: str) -> None:
        if metric not in ['l1', 'l2']:
            raise ValueError(f"Invalid metric: {metric}")

        self._metric = metric

        if not isinstance(k_neighbours, int):
            raise TypeError(f'arguments {k_neighbours} must be have type int')

        self._k_neighbours = k_neighbours

    def fit(self, abscissa: np.ndarray, labels: np.ndarray):

        if abscissa.shape[0] != labels.shape[0]:
            raise ShapeMismatchError(f"shape {abscissa.shape[0]} != shape {labels.shape[0]}")

        if not isinstance(abscissa, np.ndarray) or not isinstance(labels, np.ndarray):
            raise TypeError(" must be have type nd.ndarray")

        self._abscissa = np.array(abscissa.copy())
        self._labels = np.array(labels.copy())
        self._bool_test = True  # Флаг, указывающий на наличие тестовых данных

    def predict(self, abscissa: np.ndarray):
        if not self._bool_test:
            raise ValueError("not test data")

        if not isinstance(abscissa, np.ndarray):
            raise TypeError("must be have type nd.ndarray")

        if len(abscissa.shape) == 1:  # для broadcast
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(self._abscissa.shape[0], 1)
        # Вычисляем попарные расстояния между тестовыми и обучающими точками
        dist = distance(self._abscissa, abscissa, self._metric)
        # Вычисляем высоту окна
        wind_heigh = np.sort(dist, axis=-1)[:, self._k_neighbours]
        # Вычисляем функцию ядра для классификации
        core = np.where(np.abs(np.sort(dist, axis=-1) / wind_heigh[:, np.newaxis]) <= 1,
                        0.75 * (1 - (np.sort(dist, axis=-1) / wind_heigh[:, np.newaxis]) ** 2), 0)
        # Переупорядочиваем метки на основе расстояний
        mask = np.argsort(dist)
        self._labels = self._labels[mask]
        self._labels = self._labels[:, 0:self._k_neighbours]
        core = core[:, 0:self._k_neighbours]
        # Прогнозируем метки на основе данных
        return np.where(np.sum((self._labels - 0.5) * 2 * core, axis=1) > 0, 1, 0)
