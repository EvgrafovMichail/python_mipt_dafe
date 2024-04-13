import numpy as np


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

    mask_train = np.argsort(features_train)
    mask_test = np.argsort(features_test)

    return(
        features_train[mask_train],
        features_test[mask_test],
        targets_train[mask_train],
        targets_test[mask_test]
    )
