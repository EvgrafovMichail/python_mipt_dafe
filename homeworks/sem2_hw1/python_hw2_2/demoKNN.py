import sklearn.datasets as skd
import numpy as np
from presorting.preprocessing import test_split
from predictors.knn import KNN
from quality_marks.metric import get_accuracy_score

from utils import (
    visualize_comparison,
    freeze_random_seed,
    visualize_distribution,
    _create_diagrams,


)
freeze_random_seed()

points, labels = skd.make_blobs(
    n_samples=300, centers=3, cluster_std=2, random_state=2)
# points, labels = skd.make_moons(n_samples=400, noise=0.2)

points_train, points_test, labels_train, labels_test = test_split(
    shuffle=True,
    features=points,
    targets=labels,
    train_ratio=0.8,
)

knn = KNN(3, 3, 'l2')
knn.fit(points_train, labels_train)
prediction = knn.predict(points_test)

visualize_comparison(points_test, prediction, labels_test)
labels_unique = np.unique(labels)
for label in labels_unique:
    label_mask = labels == label
    visualize_distribution(points[label_mask], "hist", name=label)


accuracy_score = get_accuracy_score(prediction, labels_test)
print(f"knn accuracy: {accuracy_score}")
