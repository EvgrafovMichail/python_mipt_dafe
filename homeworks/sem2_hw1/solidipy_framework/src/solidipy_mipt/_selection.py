"""Common operations with data and data preprocessing.

This module contain common methods to preprocessing data.
"""

import numpy as np

from .utils.validate import check_size


def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    train_ratio: float = 0.8,
    shuffle: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split given data into training and testing samples.

    Args:
        X: The input `X` to be split.
        y: The input `y` to be split.
        train_ratio: The proportion of the data to include in the train split.
            Should be between 0.0 and 1.0. Defaults to 0.8 (80%).
        shuffle: If False, data is not shuffled. If True, data is shuffled.
            Defaults to False.

    Returns:
        X_train: The training `X`.
        X_test: The testing `X`.
        y_train: The training `y`.
        y_test: The testing `y`.

    Raises:
        ShapeMismatchError: If `X` and `y` shapes mismatch.
        ValueError: If `train_ratio` is not between 0.0 and 1.0 or not float.

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt import train_test_split
        >>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        >>> y = np.array([0, 1, 0, 1])
        >>> X_train, X_test, y_train, y_test = train_test_split(X, y, train_ratio=0.6, shuffle=True)
    """

    if shuffle:
        X, y = _shuffle_data(X, y)

    return _train_test_split(X, y, train_ratio)


def _shuffle_data(
    X: np.ndarray,
    y: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Shuffle in unison given data.

    Args:
        X: The input `X` to be split.
        y: The input `y` to be split.

    Returns:
        shuffled_X: The shuffled `X`.
        shuffle_y: The shuffled `y`.

    Raises:
        ShapeMismatchError: If `X` and `y` shapes mismatch.
    """

    check_size(X, y)

    indeces = np.random.permutation(X.shape[0])

    return X[indeces], y[indeces]


def _train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    train_ratio: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split given data into training and testing samples.

    Args:
        X: The input `X` to be split.
        y: The input `y` to be split.
        train_ratio: The proportion of the data to include in the train split.
            Should be between 0.0 and 1.0. Defaults to 0.8 (80%).

    Returns:
        X_train: The training `X`.
        X_test: The testing `X`.
        y_train: The training `y`.
        y_test: The testing `y`.

    Raises:
        ShapeMismatchError: If `X` and `y` shapes mismatch.
        ValueError: If `train_ratio` is not between 0.0 and 1.0 or not float.
    """

    check_size(X, y)

    train_ratio = float(train_ratio)
    if not (0 < train_ratio < 1):
        raise ValueError(
            "Train ration must be float between 0.0 and 1.0, "
            f"but given: {train_ratio}."
        )

    X_train, X_test = None, None
    y_train, y_test = None, None

    y_unique, indeces, counts = np.unique(y, return_index=True, return_counts=True)

    sorted_indeces = np.argsort(indeces)
    y_unique = y_unique[sorted_indeces]
    counts = counts[sorted_indeces]

    for target, count in zip(y_unique, counts):
        target_mask = y == target

        X_masked = X[target_mask]
        y_masked = y[target_mask]

        pivot = int(round(train_ratio * count))

        if X_train is None:
            X_train = X_masked[:pivot]
            X_test = X_masked[pivot:]
            y_train = y_masked[:pivot]
            y_test = y_masked[pivot:]

        else:
            X_train = np.append(
                X_train, X_masked[:pivot], axis=0
            )
            X_test = np.append(
                X_test, X_masked[pivot:], axis=0
            )
            y_train = np.append(
                y_train, y_masked[:pivot], axis=0
            )
            y_test = np.append(
                y_test, y_masked[pivot:], axis=0
            )

    if not all([X_train.any(), y_train.any()]):
        pivot = int(round(train_ratio * X_test.shape[0]))

        X_train = X_test[:pivot]
        y_train = y_test[:pivot]

    if not all([X_test.any(), y_test.any()]):
        pivot = int(round(train_ratio * X_train.shape[0]))

        X_test = X_train[:pivot]
        y_test = y_train[:pivot]

    return (
        X_train, X_test, y_train, y_test
    )
