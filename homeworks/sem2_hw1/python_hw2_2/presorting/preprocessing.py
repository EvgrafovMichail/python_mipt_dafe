import numpy as np


class ShapeMismatchError(Exception):
    pass


def test_split(
    shuffle: bool,
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f"Features shape {features.shape[0]} != targets shape {targets.shape[0]}"
        )

    if shuffle:
        mask = np.random.shuffle(np.arange(targets.shape[0]))
        features = features[mask]
        targets = targets[mask]

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
            features_train = np.append(
                features_train, target_features[:train_count], axis=0)
            features_test = np.append(
                features_test, target_features[train_count:], axis=0)
            targets_train = np.append(
                targets_train, np.full(train_count, target), axis=0)
            targets_test = np.append(targets_test, np.full(
                targets_count[target_index] - train_count, target), axis=0)

    return features_train, features_test, targets_train, targets_test
