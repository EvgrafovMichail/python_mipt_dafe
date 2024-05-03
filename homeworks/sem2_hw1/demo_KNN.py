from algorithm.knn import KNN
from metrics import Metric
from preprocessing import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from vizualize.vizualize_result import vizualize_classification
import os


dir = os.path.dirname(os.path.abspath(__file__))


def generate_data() -> list[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    x, y = make_classification(
        n_samples=5000,
        n_features=2,
        n_redundant=0,
        n_informative=2,
        random_state=1,
        n_clusters_per_class=1,
        n_classes=3
    )

    return train_test_split(x, y, shuffle=True, train_ratio=0.5)


def visualize(x: np.ndarray, y: np.ndarray, predict: np.ndarray, name: str) -> None:
    u = np.unique(y)

    _, axes = plt.subplots(1, 2, figsize=(16, 8))

    axes[0].set_title("data", fontweight='bold')
    axes[1].set_title("predict", fontweight='bold')

    for i in u:
        axes[0].scatter(x[y == i][:, 0], x[y == i][:, 1])
        axes[1].scatter(x[predict == i][:, 0], x[predict == i][:, 1])

    plt.savefig(name)


def test_KNN() -> None:
    X_train, X_test, Y_train, Y_test = generate_data()

    knn = KNN(Metric.l2, k=15, n=20)

    knn.fit(X_train, Y_train)
    prediction = knn.predict(X_train)
    print(f'train_accuracy={Metric.accuracy(Y_train, prediction)}')
    visualize(X_train, Y_train, prediction, f"{dir}/images/knn_train")

    prediction = knn.predict(X_test)
    print(f'test_accuracy={Metric.accuracy(Y_test, prediction)}')
    visualize(X_test, Y_test, prediction, f'{dir}/images/knn_test')

    vizualize_classification(X_test, Y_test, f'{dir}/images/knn_test', ['r', 'b'])


if __name__ == "__main__":
    test_KNN()
