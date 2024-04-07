import numpy as np
from typing import Iterable, Union, Any
from numbers import Real

from regressors.regressor_abc import RegressorABC
from metrics.metric import Metric


K_NEIGHBOURS = 100


class WeightedKNN(RegressorABC):
    _features: np.ndarray[float] = None
    _targets: np.ndarray[Any] = None
    _k_neighbours: int = K_NEIGHBOURS
    _distance: str = "MSE"

    def __init__(self, k_neighbours: int = K_NEIGHBOURS, distance: str = "MSE") -> None:
        k_neighbours = int(k_neighbours)

        if k_neighbours <= 0:
            raise ValueError(
                f'invalid k_neighbours value: {k_neighbours}'
                'k_neighbours could have only positive values;'
            )
        if not Metric.cheak_distances(distance):
            raise ValueError(
                f'The {distance} distance is not provided'
            )

        self._distance = distance
        self._k_neighbours = k_neighbours

    def fit(self, features: Iterable, targets: Iterable) -> None:
        if not isinstance(features, np.ndarray):
            _features = np.ndarray(features, type=float)
        else:
            _features = features
        if not isinstance(targets, np.ndarray):
            _targets = np.ndarray(targets, type=float)
        else:
            _targets = targets
        if _features.shape[0] != _targets.shape[0]:
            count_of_point = np.min(_features.shape[0], _targets.shape[0])
            _features, _targets = _features[:count_of_point], _targets[:count_of_point]

        self._features = _features
        self._targets = _targets

    def predict(self, features: Union[Real, Iterable]
                ) -> Union[Any, np.ndarray[Any]]:
        if np.any([self._features is None, self._targets is None]):
            raise RuntimeError(
                'method fit() should be called before predict():'
            )
        if isinstance(features, Real):
            return self._compute_predict(float(features))
        elif not isinstance(features, np.ndarray):
            features = np.ndarray(features)

        return np.array([self._compute_predict(i) for i in features])

    def _get_weights(self, features: np.ndarray[float]) -> np.ndarray[float]:
        distances = np.array([Metric.get_distance(features, i, self._distance)
                              for i in self._features])
        window = np.sort(distances)[self._k_neighbours - 1]
        distances = np.divide(distances, window)

        weights = np.subtract(1, np.power(distances, 2))
        weights[weights < 0] = 0
        weights = np.multiply(0.75, weights)

        return weights

    def _compute_predict(self, features: np.ndarray[Any]) -> Any:
        return np.argmax(
            np.array(
                [np.sum(self._get_weights(features)[self._targets == target])
                    for target in np.unique(self._targets)]
            )
        )
