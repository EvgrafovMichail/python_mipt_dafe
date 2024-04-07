"""
В этом модуле хранятся функции для предобработки данных
"""

import numpy as np
from data_controler.exceptions import ShapeMismatchError


def train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float = 0.8,
    shuffle: bool = False,
    classification: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f'features shape: {features.shape[0]} / targets shape: {targets.shape[0]}'
            )
    features_train, features_test, targets_train, targets_test = None, None, None, None

    if classification:
        unique_targets, proportion_targets = np.unique(targets, return_counts=True)

        for target_index, target in enumerate(unique_targets):
            target_mask = targets == target
            target_features = features[target_mask]
            if shuffle:
                np.random.shuffle(target_features)
            target_count = int(proportion_targets[target_index] * train_ratio)

            if features_train is None:
                features_train = target_features[:target_count]
                features_test = target_features[target_count:]
                targets_train = np.full(features_train.shape[0], target)
                targets_test = np.full(features_test.shape[0], target)
            else:
                features_train = np.append(features_train, target_features[:target_count], axis=0)
                features_test = np.append(features_test, target_features[target_count:], axis=0)
                targets_train = np.append(targets_train, np.full(target_count, target), axis=0)
                targets_test = np.append(targets_test, np.full(
                    proportion_targets[target_index] - target_count, target
                    ), axis=0)
    else:
        if shuffle:
            if features.ndim > 1:
                data = np.append(features, targets[..., np.newaxis], axis=1)
            else:
                data = np.append(features[..., np.newaxis], targets[..., np.newaxis], axis=1)
            np.random.shuffle(data)
            _features, _targets = np.hsplit(data, [-1])
            if features.ndim > 1:
                _targets = _targets.flatten()
            else:
                _features, _targets = _features.flatten(), _targets.flatten()
        else:
            _targets, _features = targets, features

        target_count = int(targets.size * train_ratio)
        features_train = _features[:target_count]
        features_test = _features[target_count:]
        targets_train = _targets[:target_count]
        targets_test = _targets[target_count:]

    return features_train, features_test, targets_train, targets_test
