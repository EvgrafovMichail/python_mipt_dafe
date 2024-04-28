import sklearn.datasets as skd
import numpy as np

from algo.nonparametric_regressor import NonparametricRegressor
from algo.KNN_algorithm import KNN
from separation.data_partitioning import train_test_split_nonparam, train_test_split_KNN
from quality.quality_control import MeanSquaredError, MeanAbsoluteError, R, get_accuracy_score
from visualization.KNN_vizual import visualize_comparison
from visualization.regressor_vizual import visualize_comp
from visualization.rendering import visualize_distribution
import matplotlib.pyplot as plt
from enum import Enum


FIGSIZE = (16, 9)
K_NEIGHBOURS = 4
POINTS_AMOUNT = 1000
mean = [2, 3]
cov = [[1, 1], [1, 2]]

abscissa, ordinates = np.random.multivariate_normal(mean, cov, size=1000).T
plt.style.use("ggplot")


def main() -> None:
    nonpram()
    KNN_algo()
    KNN_algo_other_colors()
    rendering_1D()
    rendering_2D()


def nonpram() -> None:
    abs = np.arange(1, POINTS_AMOUNT)
    ord = square_modulation(abs)
    abs = abs[:, np.newaxis]

    abs_train, ord_train, abs_test, ord_test = train_test_split_nonparam(abs, ord, shuffle=True)

    a = NonparametricRegressor()
    a.fit(abs_train, ord_train, K_NEIGHBOURS, 'l2')
    predict = a.predict(abs_test)
    error_ord = np.array([100000])  # коридор ошибок

    visualize_comp(abs_test.flatten(), ord_test, predict, error_ord,
                   "C:/Users/User/Desktop/nonpram.png")

    print(f'square_modulation MSE: {MeanSquaredError(ord_test, predict)}')
    print(f'square_modulation MAE: {MeanAbsoluteError(ord_test, predict)}')
    print(f'square_modulation R: {R( ord_test, predict)}')


def rendering_2D():
    my_dict = dict()
    space = 0.2
    figure = plt.figure(figsize=(8, 8))
    grid = plt.GridSpec(4, 4, wspace=space, hspace=space)

    axis_scatter = figure.add_subplot(grid[:-1, 1:])
    axis_vert = figure.add_subplot(
        grid[:-1, 0],
        sharey=axis_scatter,
    )
    axis_hor = figure.add_subplot(
        grid[-1, 1:],
        sharex=axis_scatter,
    )
    my_dict["axis_vert"] = axis_vert
    my_dict["axis_hor"] = axis_hor
    my_dict["axis_scatter"] = axis_scatter
    abscissa_2D = abscissa[:, np.newaxis]
    ordinates_2D = ordinates[:, np.newaxis]
    data = np.append(abscissa_2D, ordinates_2D, axis=1)
    type = "hist"
    visualize_distribution(my_dict, data, type,
                           "C:/Users/User/Desktop/rendering_2D.png")


def rendering_1D():
    _, axis = plt.subplots(figsize=FIGSIZE)
    type = "violin"
    visualize_distribution(axis, abscissa, type,
                           "C:/Users/User/Desktop/rendering_1D.png")


class Colors(Enum):
    BLUE = "b"
    RED = "r"
    M = "m"


def KNN_algo() -> None:
    points, labels = skd.make_moons(POINTS_AMOUNT, noise=0.6)
    points_train, points_test, labels_train, labels_test = train_test_split_KNN(
        features=points, targets=labels, train_ratio=0.7, shuffle=True
    )
    knn = KNN()
    knn.fit(points_train, labels_train, K_NEIGHBOURS)
    prediction = knn.predict(points_test)
    colors = list(Colors)
    visualize_comparison(points_test, prediction, labels_test, colors,
                         "C:/Users/User/Desktop/KNN_algo.png")

    accuracy_score = get_accuracy_score(prediction, labels_test)
    print(f"KNN accuracy: {accuracy_score}")


def KNN_algo_other_colors() -> None:
    points_test, prediction, labels_test = (np.array([[0, 0], [1, 1], [0.4, 0.4]]),
                                            np.array([0, 1, 2]),
                                            np.array([0, 2, 1]))
    colors = list(Colors)
    visualize_comparison(points_test, prediction, labels_test, colors,
                         "C:/Users/User/Desktop/KNN_algo_other_colors.png")


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
