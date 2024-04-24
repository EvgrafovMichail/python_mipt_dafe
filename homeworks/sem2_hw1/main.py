import sklearn.datasets as skd
import numpy as np


from visualization import (
    visual_regression,
    visual_knn
)
from algorithms import (
    nonparam_regression,
    train_test_split,
    linear_modulated,
    linear,
    Metric,
    knn
)
from quality_control import (
    mean_absolute_error,
    mean_squared_error,
    accuracy,
    determination_coef,
)


if __name__ == "__main__":
    # constants for generating points
    amount_of_points_for_regr = 200
    amount_of_points = 200
    lower_limit = -10
    upper_limit = 10
    index_k = 20

    abscissa = np.linspace(lower_limit, upper_limit, amount_of_points)
    to_find_abscissa = np.linspace(lower_limit, upper_limit, amount_of_points_for_regr)

    # linear prediction
    linear_points = linear(to_find_abscissa)
    linear_pred_points = nonparam_regression(
        to_find_abscissa,
        linear_points,
        index_k,
        Metric.CLASSIC
    )
    linear_mae = mean_absolute_error(linear_points[::, 1], linear_pred_points[::, 1])
    linear_mse = mean_squared_error(linear_points[::, 1], linear_pred_points[::, 1])
    linear_determination_coef = determination_coef(linear_points[::, 1], linear_pred_points[::, 1])

    # linear_modulated prediction
    linear_modulated_points = linear_modulated(to_find_abscissa)
    linear_modulated_pred_points = nonparam_regression(
        to_find_abscissa,
        linear_modulated_points,
        index_k,
        Metric.CLASSIC
    )
    linear_modulated_mae = mean_absolute_error(linear_points[::, 1], linear_pred_points[::, 1])
    linear_modulated_mse = mean_squared_error(linear_points[::, 1], linear_pred_points[::, 1])
    linear_modulated_determination_coef = determination_coef(linear_points[::, 1], linear_pred_points[::, 1])

    # regression visualisation
    visual_regression(
        linear_modulated_pred_points,
        linear_modulated_points,
        linear_mae,
        linear_mse,
        linear_determination_coef,
        "Non Linear Function",
    )
    visual_regression(
        linear_pred_points,
        linear_points,
        linear_modulated_mae,
        linear_modulated_mse,
        linear_modulated_determination_coef,
        "Linear Function",
    )

    # constants for generating points
    train_ratio = 0.8
    amount_of_points = 400
    noise = 0.3
    index_k = 20
    shuffle = True

    # knn prediction
    points, labels = skd.make_moons(n_samples=amount_of_points, noise=noise)
    train_points, train_label, test_points, test_labels = train_test_split(
        labels, points, train_ratio, shuffle,
    )
    pred_labels = knn(test_points, train_points, train_label, index_k, Metric.CLASSIC)
    knn_accuracy = accuracy(test_labels, pred_labels)

    # knn visualisation
    visual_knn(test_points, test_labels, pred_labels, knn_accuracy)
