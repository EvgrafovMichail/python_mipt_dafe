
from materials.metrics import Metrics
from materials.quality_metrics import (
    MeanAbsoluteError,
    MeanSquaredError,
    determination_coef
)
import numpy as np

from Algorithms.Nonparametric_regression import Nonparametric_regression

import sklearn.datasets as skd
from materials.split import train_test_split_nparam
from utils import (
    visualize_regression,
    visualize_comparison_nparam
)


def test_regression_linnear():

    x, y = skd.make_regression(400, 1, noise=1)
    y1 = np.reshape(y, (y.shape[0], 1))

    visualize_regression(x, y)
    points = np.concatenate((x, y1), 1)

    points_train, points_test = train_test_split_nparam(points, 0.8, True)

    assert points_train.shape[0] == 320
    assert points_test.shape[0] == 80

    x_test, y_test = np.hsplit(points_test, 2)

    n_r = Nonparametric_regression(5, Metrics[0])
    n_r.fit(points_train)
    y_predict = n_r.predict(x_test)

    y_predict = np.reshape(y_predict, (y_predict.shape[0], 1))
    print("LINNEAR:".center(100))
    print(f"MeanAbsoluteError: {MeanAbsoluteError(y_predict, y_test)};",
          f"Determination coefficient: {determination_coef(y_predict, y_test)};",
          f"MeanSquaredError: {MeanSquaredError(y_predict, y_test)}"
          )
    visualize_comparison_nparam(x_test, y_predict, y_test)


def test_regression_sinus():

    x = np.linspace(0, 1, 400)
    y = np.sin(4*np.pi*x) + np.random.normal(-0.0625, 0.0625, len(x))

    x = np.reshape(x, (x.shape[0], 1))
    y1 = np.reshape(y, (y.shape[0], 1))

    visualize_regression(x, y)
    points = np.concatenate((x, y1), 1)

    points_train, points_test = train_test_split_nparam(points, 0.8, True)

    assert points_train.shape[0] == 320
    assert points_test.shape[0] == 80

    x_test, y_test = np.hsplit(points_test, 2)

    n_r = Nonparametric_regression(5, Metrics[0])
    n_r.fit(points_train)
    y_predict = n_r.predict(x_test)

    y_predict = np.reshape(y_predict, (y_predict.shape[0], 1))

    print("SINUSOID:".center(100))
    print(f"MeanAbsoluteError: {MeanAbsoluteError(y_predict, y_test)};",
          f"Determination coefficient: {determination_coef(y_predict, y_test)};",
          f"MeanSquaredError: {MeanSquaredError(y_predict, y_test)}"
          )
    visualize_comparison_nparam(x_test, y_predict, y_test)
