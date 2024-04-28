import numpy as np
import matplotlib.pyplot as plt
from visualisation.visualize import visualize_distribution
import sklearn.datasets as skd
from materials.diagrams import diagrams


def test_vis_dist():
    x, y = skd.make_regression(400, 1, noise=1)
    y1 = np.reshape(y, (y.shape[0], 1))

    xd = plt.axes([0.5, 0.5, 0.3, 0.3])
    xd1 = plt.axes([0.1, 0.5, 0.3, 0.3])
    xd2 = plt.axes([0.5, 0.1, 0.3, 0.3])

    points = np.concatenate((x, y1), 1)
    visualize_distribution(
        [xd, xd1, xd2], points, diagrams.violin,
        "/Users/dabiz/PycharmProjects/python_mipt_dafe-3/homeworks/sem2_hw2/hahaha.png"
    )
