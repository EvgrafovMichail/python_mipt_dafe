import numpy as np
from Errors.Errors import ShapeMismatchError


def train_test_split_KNN(
    array1: np.ndarray,
    array2: np.ndarray = None,
    train_ratio: float = 0.8,
    shuffle: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    if (array1.shape[0] != array2.shape[0]) or array1.shape[0] == 0:
        raise ShapeMismatchError(
            f"Array1 shape {array1.shape[0]} != Array2 shape {array2.shape[0]}",
            "or some of the arrays has zero-shape"
        )

    return _2d(array1, array2, train_ratio, shuffle)


def _shuffle_algorithm_KNN(
    targets: np.ndarray,
    features: np.ndarray

) -> tuple[np.ndarray, np.ndarray]:

    targets_ = np.reshape(targets.copy(), (targets.shape[0], 1))
    features_ = features.copy()

    array_to_shuffle = np.append(targets_, features_, 1)

    np.random.default_rng().shuffle(array_to_shuffle, 0)

    targets_ = np.hsplit(array_to_shuffle, [1, 3])[0]
    features_ = np.hsplit(array_to_shuffle, [1, 3])[1]

    targets_ = targets_.reshape(targets.shape)

    return targets_, features_


def _2d(
    array1: np.ndarray,
    array2: np.ndarray,
    train_ratio: float,
    shuffle: bool

) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    unique_targets, targets_count = np.unique(array2, return_counts=True)
    features_train, features_test, targets_train, targets_test = None, None, None, None

    for target_index, target in enumerate(unique_targets):
        target_mask = array2 == target
        target_features = array1[target_mask]

        train_count = int(targets_count[target_index] * train_ratio)

        if features_train is None:
            features_train = target_features[:train_count]
            features_test = target_features[train_count:]
            targets_train = np.full(features_train.shape[0], target)
            targets_test = np.full(features_test.shape[0], target)
        else:
            features_train = np.append(features_train, target_features[:train_count], axis=0)
            features_test = np.append(features_test, target_features[train_count:], axis=0)
            targets_train = np.append(
                    targets_train,
                    np.full(train_count, target),
                    axis=0
            )
            targets_test = np.append(
                    targets_test,
                    np.full(targets_count[target_index] - train_count, target),
                    axis=0
            )

    if shuffle:
        targets_test, features_test = _shuffle_algorithm_KNN(targets_test, features_test)
        targets_train, features_train = _shuffle_algorithm_KNN(targets_train, features_train)

    return features_train, features_test, targets_train, targets_test


def _1d(
    array1: np.ndarray,
    train_ratio: float,
    shuffle: bool
) -> tuple[np.ndarray, np.ndarray]:

    if shuffle:
        np.random.default_rng().shuffle(array1)

    k1 = int(array1.shape[0] * train_ratio)
    array_train = array1[:k1]
    array_test = array1[k1:]

    return array_train, array_test


def train_test_split_nparam(
    array1: np.ndarray,
    train_ratio: float = 0.8,
    shuffle: bool = False
) -> tuple[np.ndarray, np.ndarray]:

    if (array1.shape[0] == 0):
        raise ShapeMismatchError(
            f"Array1 shape {array1.shape[0]} == 0"
            )

    return _1d(array1, train_ratio, shuffle)
