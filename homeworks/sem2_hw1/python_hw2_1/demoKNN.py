import sklearn.datasets as skd
from presorting.preprocessing import test_split
from predictors.knn import KNN
from quality_marks.metric import get_accuracy_score

from utils import (
    visualize_comparison,
    freeze_random_seed,
)

freeze_random_seed()

points, labels = skd.make_moons(n_samples=400, noise=0.2)

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


accuracy_score = get_accuracy_score(prediction, labels_test)
print(f"knn accuracy: {accuracy_score}")
