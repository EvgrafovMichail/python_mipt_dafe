import sklearn.datasets as skd
import numpy as np
from visualisation.visualize import visualize_regression


def test_vis_regr():

    x, y, _ = skd.make_regression(100, 1, noise=10, coef=True)
    y1 = np.reshape(y, (y.shape[0], 1))
    y2 = x*_
    y3 = y2 + 10
    y4 = y2 - 10

    points = np.concatenate((x, y1), 1)
    trend = np.concatenate((x, y2), 1)
    error_corridor1 = np.concatenate((x, y3), 1)
    error_corridor2 = np.concatenate((x, y4), 1)
    visualize_regression(points, trend, (error_corridor1, error_corridor2))
