import numpy as np
import sklearn.datasets as skd

from algorithms import (
    train_test_split,
    KNN
)
from utils import (
    visualize_comparison,
    freeze_random_seed,
    get_accuracy_score
)

freeze_random_seed()
points, labels = skd.make_moons(n_samples=400, noise=0.3)


def testing_knn(
        knn: KNN,
        points: np.array = points,
        labels: np.array = labels):

    points_train, points_test, labels_train, labels_test = train_test_split(
        features=points,
        targets=labels,
        train_ratio=0.8,
        shuffle=True
    )

    knn.fit(points_train, labels_train)
    prediction = knn.predict(points_test)
    visualize_comparison(points_test, prediction, labels_test)

    accuracy = get_accuracy_score(prediction, labels_test)
    print(f'KNN accuracy = {accuracy}')
