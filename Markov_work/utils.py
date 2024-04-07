import sklearn.datasets as skd
import numpy as np

from algorithms.nonparametric_regressor import NonparametricRegressor
from algorithms.KNN_algorithm import KNN
from algorithms.data_partitioning import train_test_split_nonparam, train_test_split_KNN
from algorithms.quality_control import MeanSquaredError, MeanAbsoluteError, R, get_accuracy_score


K_NEIGHBOURS = 3
POINTS_AMOUNT = 100


def main() -> None:
    nonpram()
    KNN_algo()


def nonpram() -> None:
    abs = np.arange(1, POINTS_AMOUNT)
    ord = square_modulation(abs)
    abs = abs[:, np.newaxis]

    abs_train, ord_train, abs_test, ord_test = train_test_split_nonparam(abs, ord, shuffle=True)

    a = NonparametricRegressor()
    a.fit(abs_train, ord_train, K_NEIGHBOURS, 'l2')
    predict = a.predict(abs_test)

    print(f'square_modulation MSE: {MeanSquaredError(ord_test, predict)}')
    print(f'square_modulation MAE: {MeanAbsoluteError(ord_test, predict)}')
    print(f'square_modulation R: {R( ord_test, predict)}')


def KNN_algo() -> None:
    points, labels = skd.make_moons(POINTS_AMOUNT, noise=0.6)
    points_train, points_test, labels_train, labels_test = train_test_split_KNN(
                                                                                features=points,
                                                                                targets=labels,
                                                                                train_ratio=0.7,
                                                                                shuffle=True
                                                                                )
    knn = KNN()
    knn.fit(points_train, labels_train, K_NEIGHBOURS)
    prediction = knn.predict(points_test)
    accuracy_score = get_accuracy_score(prediction, labels_test)
    print(f"KNN accuracy: {accuracy_score}")


def linear_modulation(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def square_modulation(abscissa: np.ndarray) -> np.ndarray:
    function_values = abscissa ** 2 + abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def radical_modulation(abscissa: np.ndarray) -> np.ndarray:
    function_values = abscissa ** 0.5
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise
