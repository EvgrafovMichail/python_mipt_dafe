import numpy as np


def _shuffle(
    X: np.ndarray,
    y: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    mask = np.random.permutation(X.shape[0])
    return X[mask], y[mask]


def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    train_ratio: float = 0.8,
    shuffle: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    if not (0 < train_ratio < 1):
        raise ValueError("train ratio must be > 0 and < 1")

    if (shuffle):
        _shuffle(X, y)

    if (X.shape[0] != y.shape[0]):
        raise ValueError("X and y have different dim")

    features_train, features_test = None, None
    targets_train, targets_test = None, None

    targets_unique, counts = np.unique(y, return_counts=True)

    for target, count in zip(targets_unique, counts):
        target_mask = y == target

        features_masked = X[target_mask]
        targets_masked = y[target_mask]

        pivot = int(round(train_ratio * count))

        if features_train is None:
            features_train = features_masked[:pivot]
            features_test = features_masked[pivot:]
            targets_train = targets_masked[:pivot]
            targets_test = targets_masked[pivot:]

        else:
            features_train = np.append(
                features_train, features_masked[:pivot], axis=0
            )
            features_test = np.append(
                features_test, features_masked[pivot:], axis=0
            )
            targets_train = np.append(
                targets_train, targets_masked[:pivot], axis=0
            )
            targets_test = np.append(
                targets_test, targets_masked[pivot:], axis=0
            )

    return (
        features_train, features_test, targets_train, targets_test
    )
