import numpy as np

from sci_fw.helpers.data import check_array, check_shapes


def accuracy_ratio(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    prediction = check_array(prediction)
    expectation = check_array(expectation)
    check_shapes(prediction, expectation)

    matches = (prediction == expectation).sum()
    accuracy_ratio = matches / prediction.shape[0]
    return accuracy_ratio


def MSE(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    prediction = check_array(prediction)
    expectation = check_array(expectation)
    check_shapes(prediction, expectation)

    mse = (prediction - expectation) ** 2
    mse = mse.sum() / mse.shape[0]
    return mse


def MAE(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    prediction = check_array(prediction)
    expectation = check_array(expectation)
    check_shapes(prediction, expectation)

    mae = np.abs((prediction - expectation))
    mae = mae.sum() / mae.shape[0]
    return mae


def determination_coef(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    prediction = check_array(prediction)
    expectation = check_array(expectation)
    check_shapes(prediction, expectation)

    mean = expectation.mean()
    r2 = ((prediction - expectation) ** 2).sum()
    r2 /= ((expectation - mean) ** 2).sum()
    r2 = 1 - r2
    return r2
