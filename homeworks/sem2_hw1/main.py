import numpy as np
from typing import Union


class ShapeMismatchError(Exception):
    pass


def distance(t_abscissa: np.ndarray, abscissa: np.ndarray, metric: str) -> np.ndarray:
    if metric == 'l1':
        dist = np.linalg.norm(t_abscissa - abscissa[:, np.newaxis], axis=2, ord=1)

    elif metric == 'l2':
        dist = np.linalg.norm(
            t_abscissa - abscissa[:, np.newaxis], axis=2)
    return dist


def train_test_split(
        features: np.ndarray,
        targets: np.ndarray,
        shuf: bool,
        train_ratio: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f"Features shape {features.shape[0]} != targets shape {targets.shape[0]}"
        )
    if shuf:
        indices = np.arange(features.shape[0])
        np.random.shuffle(indices)
        features = features[indices]
        targets = targets[indices]

    unique_targets, targets_count = np.unique(targets, return_counts=True)
    features_train, features_test, targets_train, targets_test = None, None, None, None

    for target_index, target in enumerate(unique_targets):
        target_mask = targets == target
        target_features = features[target_mask]
        train_count = int(targets_count[target_index] * train_ratio)

        if features_train is None:
            features_train = target_features[:train_count]
            features_test = target_features[train_count:]
            targets_train = np.full(features_train.shape[0], target)
            targets_test = np.full(features_test.shape[0], target)
        else:
            features_train = np.append(features_train, target_features[:train_count], axis=0)
            features_test = np.append(features_test, target_features[train_count:], axis=0)
            targets_train = np.append(targets_train, np.full(train_count, target), axis=0)
            targets_test = np.append(
                targets_test, np.full(targets_count[target_index] - train_count, target), axis=0
                )

    return features_train, features_test, targets_train, targets_test


class NREGR:
    _k_neighbours: int
    _metric: str
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

        self._abscissa = abscissa
        self._ordinates = ordinates
        self._bool_test = True

    def predict(self, abscissa: np.ndarray):
        if not self._bool_test:
            raise ValueError("not test data")

        if not isinstance(abscissa, np.ndarray):
            raise TypeError("must be have type nd.ndarray")

        if len(abscissa.shape) == 1:  # для broadcast
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(self._abscissa.shape[0], 1)

        dist = distance(self._abscissa, abscissa, self._metric)

        wind_heigh = np.sort(dist, axis=-1)[:, self._k_neighbours]

        core = np.where(np.abs(dist / wind_heigh[:, np.newaxis]) <= 1,
                        0.75 * (1 - (dist / wind_heigh[:, np.newaxis]) ** 2), 0)

        return np.sum(self._ordinates * core, axis=1) / np.sum(core, axis=1)


class KNN:
    _k_neighbours: int
    _metric: str
    _abscissa: np.ndarray
    _ordinates: np.ndarray

    def __init__(self, k_neighbours: int, metric: str) -> None:
        if metric not in ['l1', 'l2']:
            raise ValueError(f"not correct metric {metric}")

        self._metric = metric

        if not isinstance(k_neighbours, int):
            raise TypeError(f'arguments {k_neighbours} must be have type int')

        self._k_neighbours = k_neighbours

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray):

        if abscissa.shape[0] != ordinates.shape[0]:
            raise ShapeMismatchError(f"shape {abscissa.shape[0]} != shape {ordinates.shape[0]}")

        if not isinstance(abscissa, np.ndarray) or not isinstance(ordinates, np.ndarray):
            raise TypeError(" must be have type nd.ndarray")

        self._abscissa = abscissa
        self._ordinates = ordinates
        self._bool_test = True

    def predict(self, abscissa: np.ndarray):
        if not self._bool_test:
            raise ValueError("not test data")

        if not isinstance(abscissa, np.ndarray):
            raise TypeError("must be have type nd.ndarray")

        if len(abscissa.shape) == 1:  # для broadcast
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(self._abscissa.shape[0], 1)

        dist = distance(self._abscissa, abscissa, self._metric)

        wind_heigh = np.sort(dist, axis=-1)[:, self._k_neighbours]

        core = np.where(np.abs(np.sort(dist, axis=-1) / wind_heigh[:, np.newaxis]) <= 1,
                        0.75 * (1 - (np.sort(dist, axis=-1) / wind_heigh[:, np.newaxis]) ** 2), 0)

        mask = np.argsort(dist)
        self._ordinates = self._ordinates[mask]
        self._ordinates = self._ordinates[:, 0:self._k_neighbours]
        core = core[:, 0:self._k_neighbours]

        return np.where(np.sum((self._ordinates - 0.5) * 2 * core, axis=1) > 0, 1, 0)


def MSE(y_pred: np.ndarray, y_true: np.ndarray):
    s = np.mean((y_true - y_pred) ** 2)
    return s


def MAE(y_pred: np.ndarray, y_true: np.ndarray):
    s = np.mean(np.abs(y_true - y_pred))
    return s


def rr(y_pred: np.ndarray, y_true: np.ndarray):
    return 1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)


def accuracy(y_pred: np.ndarray, y_true: np.ndarray):
    return np.mean(y_true == y_pred)
