"""Metrics for algorithm analysis.

This module ...

Example:
    from solidipy.examples import metrics

    
    if __name__ == "__main__":
        metrics.start()
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
        predication: 
        expectation:
    
    Returns:
        mse_score: MSE score for given data.
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
        predication: 
        expectation:
    
    Returns:
        mae_score: MAE score for given data.
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
        predication: 
        expectation:
    
    Returns:
        dc_score: DC score for given data.
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
        predication: 
        expectation:
    
    Returns:
        accuracy: Accuracy score for given data.
    """

    check_size(prediction, expectation)
    
    return np.sum(prediction == expectation) / prediction.shape[0]