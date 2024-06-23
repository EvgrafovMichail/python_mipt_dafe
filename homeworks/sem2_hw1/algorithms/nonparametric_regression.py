import numpy as np
from typing import Union
from metric_distances import distance
from precompilation import ShapeMismatchError


class NPR:
    def __init__(self, k_neighbours: int, metric: str) -> None:
        if metric not in ['l1', 'l2']:
            raise ValueError(f"Invalid metric: {metric}")

        self._k_neighbours = k_neighbours
        self._metric = metric
        self._abscissa: Union[np.ndarray, None] = None
        self._ordinates: Union[np.ndarray, None] = None
        self._bool_test = False

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray) -> None:
        if abscissa.shape[0] != ordinates.shape[0]:
            raise ShapeMismatchError(f"Shape {abscissa.shape[0]} != shape {ordinates.shape[0]}")

        self._abscissa = np.array(abscissa.copy())
        self._ordinates = np.array(ordinates.copy())
        self._bool_test = True

    def predict(self, abscissa: np.ndarray) -> np.ndarray:
        if not self._bool_test:
            raise ValueError("Not test data")

        if len(abscissa.shape) == 1:
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(self._abscissa.shape[0], 1)

        dist = distance(self._abscissa, abscissa, self._metric)
        wind_heigh = np.sort(dist, axis=-1)[:, self._k_neighbours]
        core = np.where(np.abs(dist / wind_heigh[:, np.newaxis]) <= 1,
                        0.75 * (1 - (dist / wind_heigh[:, np.newaxis]) ** 2), 0)
        return np.sum(self._ordinates * core, axis=1) / np.sum(core, axis=1)
