"""Common operations with data and data preprocessig.

This module ...

Example:
    from solidipy.examples import data_preprocessing

    
    if __name__ == "__main__":
        data_preprocessing.start()
"""

import numpy as np

from .utils.errors import ShapeMismatchError
from .utils.validate import check_size


def train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float = 0.8,
    shuffle: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split given data to train and test samples.

    Args:
        features: 
        targets:
        train_ratio: between 0 and 1
        shuffle: 
    
    Returns:
        features_train:
        features_test:
        targets_train:
        targets_test:
    """

    check_size(features, targets)
    
    if not (0 < train_ratio < 1):
        raise ValueError("train ration must be float between 0 and 1")
    
    if shuffle:
        features, targets = _shuffle_data(features, targets)

    return _train_test_split(features, targets, train_ratio)


def _shuffle_data(
    features: np.ndarray,
    targets: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Shuffle in unison given data.
    Args:
        features: 
        targets:
    
    Returns:
        shuffled_features:
        shuffle_targets:
    """

    check_size(features, targets)
    
    indeces = np.random.permutation(features.shape[0])

    return features[indeces], targets[indeces]


def _train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split given data to train and test samples.

    Args:
        features: 
        targets:
        train_ratio: between 0 and 1
    
    Returns:
        features_train:
        features_test:
        targets_train:
        targets_test:
    """

    check_size(features, targets)

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

    return (
        features_train, features_test, targets_train, targets_test
    )
