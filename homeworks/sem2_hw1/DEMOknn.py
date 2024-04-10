import sklearn.datasets as skd
from preprocessing import test_split
from knn import KNN
from estimation import print_estimation
from random_seed import freeze_random_seed
from visualize import visualize_comparison


def main():     # написан Евграфовым в первом семестре
    freeze_random_seed()

    points, labels = skd.make_moons(n_samples=400, noise=0.2)

    points_train, points_test, labels_train, labels_test = test_split(
        shuffle=True,
        features=points,
        targets=labels,
        train_ratio=0.8,
    )

    knn = KNN(3, 'l2')
    knn.fit(points_train, labels_train)
    prediction = knn.predict(points_test)

    visualize_comparison(points_test, prediction, labels_test)
    print_estimation(prediction, labels_test)


main()
