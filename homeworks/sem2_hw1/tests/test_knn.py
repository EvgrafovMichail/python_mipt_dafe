
from materials.metrics import Metrics
from materials.quality_metrics import get_accuracy_score
import numpy as np

from Algorithms.KNN_with_weights import KNN

import sklearn.datasets as skd
from materials.split import train_test_split_KNN
from utils import (
    visualize_comparison,
    visualize_scatter,
)


def test_knn():
    points, labels = skd.make_moons(n_samples=400, noise=0.3)
    visualize_scatter(points, labels)

    points_train, points_test, labels_train, labels_test = train_test_split_KNN(
        points,
        labels,
        train_ratio=0.8,
        shuffle=True
    )

    assert points_train.shape[0] == labels_train.shape[0]
    assert points_train.shape[0] == 320
    assert points_test.shape[0] == labels_test.shape[0]
    assert points_test.shape[0] == 80

    for label_part in (labels_test, labels_train):
        _, counts = np.unique(label_part, return_counts=True)
        assert counts[0] == counts[-1]

    knn = KNN(5, Metrics[0])
    knn.fit(points_train, labels_train)
    prediction = knn.predict(points_test)

    visualize_comparison(points_test, prediction, labels_test)

    accuracy_score = get_accuracy_score(prediction, labels_test)
    print(f"knn accuracy: {accuracy_score}")
