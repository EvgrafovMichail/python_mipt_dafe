# import numpy as np
# from preprocessing.get_boxplot_outliers import get_boxplot_outliers
from classific.Classificator import Classificator
from preprocessing.preprocessing import train_test_split
from metrics import accuracy, precision_score, recall_score, f1_score
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt
from utils import (
    visualize_comparison,
    freeze_random_seed,
)
from graphics.visualize_distribution import visualize_distribution
from graphics.classification_plot import classification_plot
freeze_random_seed()


def show(points, labels, y_pred):

    visualize_comparison(points, y_pred, labels)
    plt.show()


def main():

    width = 10
    norm = "l2"
    k_numbers = 100
    n_sample = 1000

    x, y = make_moons(n_samples=n_sample, noise=0.3)
    print(x.shape, y.shape)

    # y_ = y.reshape(y.shape[0], 1)
    # data = np.hstack([x, y_]).T

    """
    outliters = get_boxplot_outliers(data, np.sort)
    y_out = data[-1][outliters]
    data_out = data[data[-1] == y_out]
    """

    knn = Classificator(width, k_numbers, norm)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, shuffle=True)

    knn.fit(x_train, y_train)
    y_pred = knn.predict(x_test)

    show(x_test, y_pred, y_test)

    classification_plot(x, y, "images/class.jpg", ["red", "green", "blue"])
    # classification_plot(x_out, y_out,"images/class.jpg",
    # ["red", "yellow"], True)

    print(f"Accuracy score is --- {accuracy(y_pred, y_test)}")

    print(f"Precision score is --- {precision_score(y_pred, y_test)}")

    print(f"Recall score is --- {recall_score(y_pred, y_test)}")

    print(f"F1 score is --- {f1_score(y_pred, y_test)}")

    print(x.ndim)

    visualize_distribution(x.T, "vioLiN", "images/classification.png")


main()
