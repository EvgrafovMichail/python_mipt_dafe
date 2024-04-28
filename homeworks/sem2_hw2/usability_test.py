# flake8: noqa

import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Callable

from ultralib999.UltraVisualisator999 import *
from ultralib999.TrainTestSplit import train_test_split
from ultralib999.QualityMetrics import mse, mae, r_pow_2, accuracy
import sklearn.datasets as skd
from ultralib999.Algorithms import get_boxplot_outliers, KNN
from ultralib999.GlobalVars import DistanceMetrics


def demo_visualise():
    path_to_save = "C:\\Users\\botin\\PycharmProjects\\python_mipt_dafe\\homeworks\\sem2_hw2\\tmp_results\\"
    # generating points for scatter
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]

    data = np.random.multivariate_normal(mean, cov, size=1000)

    # 2-dim
    figure = plt.figure(figsize=(16, 9))
    grid = plt.GridSpec(4, 4, wspace=0.2, hspace=0.2)

    axis_scatter = figure.add_subplot(grid[:-1, 1:])
    axis_hist_vert = figure.add_subplot(
        grid[:-1, 0],
        sharey=axis_scatter,
    )
    axis_hist_hor = figure.add_subplot(
        grid[-1, 1:],
        sharex=axis_scatter,
    )
    axises = [axis_scatter, axis_hist_vert, axis_hist_hor]
    visualize_distribution(axises, data, "hist", path_to_save=path_to_save)

    # 1-dim data
    data = np.random.normal(10, 10, 500)
    _, axus = plt.subplots(figsize=(16, 9))
    visualize_distribution(axus, data, "hist", path_to_save=path_to_save + "1d_data.png")
    # 4-dim data
    data = np.random.normal(10, 10, (500, 4))
    _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 9))
    x = [ax1, ax2, ax3, ax4]
    visualize_distribution(x, data, "boxplot", path_to_save=path_to_save + "4d_data.png")


def demo_knn():
    norm = DistanceMetrics.L2
    k_numbers = 8
    n_sample = 1000

    x, y = skd.make_moons(n_samples=n_sample, noise=0.6)
    knn = KNN(5, k_numbers, norm)
    x_train, x_test, y_train, y_test = train_test_split(x, y)

    knn.fit(x_train, y_train)
    y_pred = knn.predict(x_test)

    x2, y2 = skd.make_moons(n_samples=n_sample, noise=0.6)
    knn = KNN(5, k_numbers, norm)
    x_train, x_test2, y_train, y_test2 = train_test_split(x, y)

    knn.fit(x_train, y_train)
    y_pred2 = knn.predict(x_test2) + 204863

    xy_final = np.vstack((x_test, x_test2))
    y_pred_final = np.hstack((y_pred, y_pred2)).T
    print(xy_final.shape, y_pred_final.shape)

    figure = plt.figure(figsize=(8, 8))
    axis = figure.add_subplot()
    axis.set_title("classification", fontweight='bold')
    visualize_classification(axis, xy_final, y_pred_final, ["orange", "green", "blue", "red", "black"])


def megazavr(x):
    return (x ** 2) * np.sin(x)


def make_regression_data(function, n_sample, noise):
    x = np.linspace(1, 10, n_sample)
    y = function(x)
    if (noise):
        y += np.random.normal(size=x.size, scale=0.05)
    return x, y


def demo_npr():
    n_sample = 1000
    noise = True
    function = megazavr

    x, y = make_regression_data(function, n_sample, False)
    sigma = 10

    figure = plt.figure(figsize=(8, 8))
    axis = figure.add_subplot()
    axis.set_title("classification", fontweight='bold')
    data = np.hstack((x, y))
    # visualize_distribution(axis, data, "hist")
    err = np.vstack((y - sigma, y + sigma))
    visualize_regression(axis, x, y, err)


def get_boxplot_outliers2(
        data: np.ndarray,
        key: Callable[[Any], Any] = "quicksort",
) -> np.ndarray:
    if not (isinstance(data, np.ndarray)):
        raise ValueError("data must be a np.ndarray")

    keys = ["quicksort", "mergesort", "heapsort", "stable"]
    if not (key in keys):
        raise ValueError(f"{key} doesn't exist")

    indexes_sorted = np.argsort(data, kind=key, axis=0)
    data_sorted = np.sort(data, kind=key, axis=0)

    # abscissa
    abscissa_indexes_sorted = indexes_sorted[::, 0]
    abscissa_sorted = data_sorted[::, 0]

    abscissa_quartile1 = int(abscissa_sorted[int(len(abscissa_sorted) * 0.25)])
    abscissa_quartile3 = int(abscissa_sorted[int(len(abscissa_sorted) * 0.75)])
    abscissa_epsilon = int((abscissa_quartile3 - abscissa_quartile1) * 1.5)

    abscissa_lower = abscissa_sorted < abscissa_quartile1 - abscissa_epsilon
    abscissa_upper = abscissa_sorted > abscissa_quartile3 + abscissa_epsilon

    abscissa_indexes_cut = np.append(
        abscissa_indexes_sorted[abscissa_lower],
        abscissa_indexes_sorted[abscissa_upper],
    )

    # ordinates
    ordinates_indexes_sorted = indexes_sorted[::, 1]
    ordinates_sorted = data_sorted[::, 1]

    ordinates_quartile1 = round(ordinates_sorted[int(len(ordinates_sorted) * 0.25)])
    ordinates_quartile3 = round(ordinates_sorted[int(len(ordinates_sorted) * 0.75)])
    ordinates_epsilon = int((ordinates_quartile3 - ordinates_quartile1) * 1.5)

    ordinates_lower = ordinates_sorted < ordinates_quartile1 - ordinates_epsilon
    ordinates_upper = ordinates_sorted > ordinates_quartile3 + ordinates_epsilon

    ordinates_indexes_cut = np.append(
        ordinates_indexes_sorted[ordinates_lower],
        ordinates_indexes_sorted[ordinates_upper],
    )

    return abscissa_indexes_cut, ordinates_indexes_cut


def box_outliers():
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]

    data = np.random.multivariate_normal(mean, cov, size=200)
    print(data)

    extras = get_boxplot_outliers(data, "quicksort")
    print(f"extras emissions: {extras}")
    print("\n\n")
    abscs, ordin = get_boxplot_outliers2(data, "quicksort")
    print(f"abscissa emissions: {abscs}")
    print(f"ordinates emissions: {ordin}")


box_outliers()
