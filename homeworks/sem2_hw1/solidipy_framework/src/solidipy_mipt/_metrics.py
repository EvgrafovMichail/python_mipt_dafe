"""Metrics for algorithm analysis.

This module calculates evaluation metrics based on predicted and expected data.
"""

import numpy as np

from .utils.validate import check_size


def mse(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    """
    Calculate MSE(Mean Squared Value) score for given data.

    Args:
        predication: The predicted target values from a model.
        expectation: The true (expected) target values.

    Returns:
        mse_score: MSE score for given data.

    Raises:
        ShapeMismatchError: If prediction and expectation shapes mismatch.

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt import mse
        >>> y_true = np.array([1, 0, 1, 1, 0])
        >>> y_pred = np.array([1, 1, 1, 0, 0])
        >>> mse_score = mse(y_pred, y_true)
        >>> print(mse_score)
    """

    check_size(prediction, expectation)

    return np.sum((prediction - expectation) ** 2) / prediction.shape[0]


def mae(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    """
    Calculate MAE(Mean Absolute Error) score for given data.

    Args:
        predication: The predicted target values from a model.
        expectation: The true (expected) target values.

    Returns:
        mae_score: MAE score for given data.

    Raises:
        ShapeMismatchError: If prediction and expectation shapes mismatch.

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt import mae
        >>> y_true = np.array([1, 0, 1, 1, 0])
        >>> y_pred = np.array([1, 1, 1, 0, 0])
        >>> mae_score = mae(y_pred, y_true)
        >>> print(mae_score)
    """

    check_size(prediction, expectation)

    return np.sum(np.absolute(prediction - expectation)) / prediction.shape[0]


def dc(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    """
    Calculate DC(Determination Coefficient) score for given data.

    Args:
        predication: The predicted target values from a model.
        expectation: The true (expected) target values.

    Returns:
        dc_score: DC score for given data.

    Raises:
        ShapeMismatchError: If prediction and expectation shapes mismatch.

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt import dc
        >>> y_true = np.array([1, 0, 1, 1, 0])
        >>> y_pred = np.array([1, 1, 1, 0, 0])
        >>> dc_score = dc(y_pred, y_true)
        >>> print(dc_score)
    """

    check_size(prediction, expectation)

    squared_error = np.sum((prediction - expectation) ** 2)
    mean_error = np.sum((prediction - np.mean(prediction)) ** 2)

    return 1 - (squared_error / mean_error)


def accuracy(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    """
    Calculate Accuracy score for given data.

    Args:
        predication: The predicted target values from a model.
        expectation: The true (expected) target values.

    Returns:
        accuracy_score: Accuracy score for given data.

    Raises:
        ShapeMismatchError: If prediction and expectation shapes mismatch.

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt import accuracy
        >>> y_true = np.array([1, 0, 1, 1, 0])
        >>> y_pred = np.array([1, 1, 1, 0, 0])
        >>> accuracy_score = accuracy(y_pred, y_true)
        >>> print(accuracy_score)
    """

    check_size(prediction, expectation)

    return np.sum(prediction == expectation) / prediction.shape[0]
