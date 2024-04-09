import numpy as np
from classific.Classificator import Classificator
from preprocessing import train_test_split
from metrics import accuracy, precision_score, recall_score, f1_score
from sklearn.datasets import make_classification, make_moons
import itertools
import matplotlib.pyplot as plt
from utils import (
    visualize_comparison,
    visualize_scatter,
    freeze_random_seed,
)

freeze_random_seed()

def show(points, labels, y_pred):

    #plt.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)
    #visualize_scatter(points, labels)
    visualize_comparison(points, y_pred, labels)
    plt.show()


def main():

    width = 3
    norm = "l2"
    k_numbers = 8
    n_sample = 1000

    #x, y = make_classification(random_state=42)
    x, y = make_moons(n_samples=n_sample, noise=0.2)

    knn = Classificator(width , k_numbers, norm)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, shuffle = True)

    knn.fit(x_train, y_train)
    y_pred = knn.predict(x_test)

    show(x_test, y_pred, y_test)

    print(f"Accuracy score is --- {accuracy(y_pred, y_test)}")

    print(f"Precision score is --- {precision_score(y_pred, y_test)}")

    print(f"Recall score is --- {recall_score(y_pred, y_test)}")

    print(f"F1 score is --- {f1_score(y_pred, y_test)}")

main()