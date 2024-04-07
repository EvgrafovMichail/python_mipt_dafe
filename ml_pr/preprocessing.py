import numpy as np
import random

class ShapeMismatchError(Exception):
    pass

def train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float = 0.8,
    shuffle = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f"Features shape {features.shape[0]} \
            != targets shape {targets.shape[0]}"
        )
    
    if train_ratio <= 0 or 1 <= train_ratio:
        raise ValueError("train ration must be float between 0 and 1")
    
    if(shuffle):
        size = targets.shape[0]
        rand_num = np.random.shuffle(np.arange(size))
        features, targets = features[rand_num], targets[rand_num]

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

    return (features_train, features_test, targets_train, targets_test)