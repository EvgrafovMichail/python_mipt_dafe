import numpy as np
from typing import Union
from metric_distances import distance
from precompilation import ShapeMismatchError


class KNN:
    def __init__(self, k_neighbours: int, metric: str) -> None:
        if metric not in ['l1', 'l2']:
            raise ValueError(f"Invalid metric: {metric}")

        self._k_neighbours = k_neighbours
        self._metric = metric
        self._abscissa: Union[np.ndarray, None] = None
        self._labels: Union[np.ndarray, None] = None
        self._bool_test = False

    def fit(self, abscissa: np.ndarray, labels: np.ndarray) -> None:
        if abscissa.shape[0] != labels.shape[0]:
            raise ShapeMismatchError(f"Shape {abscissa.shape[0]} != shape {labels.shape[0]}")

        self._abscissa = np.array(abscissa.copy())
        self._labels = np.array(labels.copy())
        self._bool_test = True

    def predict(self, abscissa: np.ndarray) -> np.ndarray:
        if not self._bool_test:
            raise ValueError("Not test data")

        if len(abscissa.shape) == 1:
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(self._abscissa.shape[0], 1)

        dist = distance(self._abscissa, abscissa, self._metric)
        wind_heigh = np.sort(dist, axis=-1)[:, self._k_neighbours]
        core = np.where(np.abs(np.sort(dist, axis=-1) / wind_heigh[:, np.newaxis]) <= 1,
                        0.75 * (1 - (np.sort(dist, axis=-1) / wind_heigh[:, np.newaxis]) ** 2), 0)
        mask = np.argsort(dist)
        self._labels = self._labels[mask]
        self._labels = self._labels[:, 0:self._k_neighbours]
        core = core[:, 0:self._k_neighbours]
        return np.where(np.sum((self._labels - 0.5) * 2 * core, axis=1) > 0, 1, 0)
