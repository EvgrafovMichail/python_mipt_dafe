from knn import KNN
import sklearn.datasets as skd
from preprocess import train_test_split
from accuracy import get_accuracy_score

from utils import (
    visualize_comparison,
    freeze_random_seed,
)

freeze_random_seed()

points, labels = skd.make_moons(n_samples=400, noise=0.3)
#visualize_scatter(points, labels)

points_train, points_test, labels_train, labels_test = train_test_split(
    features=points,
    targets=labels,
    train_ratio=0.8,
    shuffle=True
)


knn = KNN()
knn.fit(points_train, labels_train)
prediction = knn.predict(points_test)

visualize_comparison(points_test, prediction, labels_test)

accuracy = get_accuracy_score(prediction, labels_test)
print(f'KNN accuracy = {accuracy}')