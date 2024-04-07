import numpy as np

NDIGITS = 4


def MeanSquaredError(real_value: np.array, predict_value: np.array):
    tmp = real_value - predict_value
    tmp = tmp ** 2
    tmp /= len(tmp)
    tmp = np.sum(tmp)

    return round(tmp, NDIGITS)


def MeanAbsoluteError(real_value: np.array, predict_value: np.array):
    tmp = real_value - predict_value
    tmp = np.abs(tmp)
    tmp /= len(tmp)
    tmp = np.sum(tmp)

    return round(tmp, NDIGITS)


def R(real_value: np.array, predict_value: np.array):
    tmp1 = real_value - predict_value
    tmp1 = np.sum(tmp1 ** 2)

    tmp2 = predict_value - np.mean(real_value)
    tmp2 = np.sum(tmp2 ** 2)
    r = 1 - tmp1/tmp2

    return r


def get_accuracy_score(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    accuracy = np.sum(prediction == expectation) / len(prediction)

    return round(accuracy, NDIGITS)
