import numpy as np
from typing import Callable, Any


class ShapeMismatchError(Exception):
    pass


def train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    shuffle: bool = True,
    train_ratio: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f"Features shape {features.shape[0]} != targets shape {targets.shape[0]}"
        )

    if shuffle:
        mask = np.arange(targets.shape[0])
        np.random.shuffle(mask)
        features = features[mask]
        targets = targets[mask]

    train_count = int(features.shape[0] * train_ratio)
    features_train = features[:train_count]
    features_test = features[train_count:]
    targets_train = targets[:train_count]
    targets_test = targets[train_count:]

    if (features.ndim == 1):
        mask_train = np.argsort(features_train)
        mask_test = np.argsort(features_test)

        features_train = features[mask_train]
        features_test = features[mask_test]
        targets_train = targets[mask_train]
        targets_test = targets[mask_test]

    return(
        features_train,
        features_test,
        targets_train,
        targets_test
    )


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
    cmp: Callable[[Any], Any]    
) -> np.ndarray:
    data = key(data)
    q1 = data[int(data.shape[0] * 0.25)]
    q3 = data[int(data.shape[0] * 0.75)]
    e = (q3 - q1) * 1.5
    res = np.argwhere((cmp(data, (q1-e).reshape(1, *e.shape)) == 1) * (cmp(data, (q3+e).reshape(1, *e.shape) == 0)))

    return res


def key(a):
    return np.sort(a, axis=0)


def cmp(a, b):
    return a[:, 1] > b[0, 1]


if __name__ == "__main__":
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]
    space = 0.2

    print(get_boxplot_outliers(np.random.multivariate_normal(mean, cov, size=1000), key, cmp))