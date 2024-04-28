import numpy as np


class ShapeMismatchError(Exception):
    pass


def train_test_split(
        features: np.ndarray,
        targets: np.ndarray,
        train_ratio: float = 0.8,
        shuffle: bool = True,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError

    if train_ratio <= 0 or 1 <= train_ratio:
        raise ValueError("train ration must be float between 0 and 1")

    if not isinstance(shuffle, bool):
        raise ValueError("Shuffle must be a bool")

    if shuffle:
        shuffled_indexes = np.arange(0, features.shape[0])
        np.random.shuffle(shuffled_indexes)
        features = features[shuffled_indexes]
        targets = targets[shuffled_indexes]

    features_train, features_test = None, None
    targets_train, targets_test = None, None

    targets_unique, counts = np.unique(targets, return_counts=True)

    for target, count in zip(targets_unique, counts):
        target_mask = targets == target

        features_masked = features[target_mask]
        targets_masked = targets[target_mask]

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

    return features_train, features_test, targets_train, targets_test
