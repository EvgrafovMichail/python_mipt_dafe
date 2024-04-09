import sklearn.datasets as skd

from algorithms import (
    nonparametric_regression,
    testing_nr,
    KNN,
    testing_knn
)


if __name__ == '__main__':
    points, labels = skd.make_moons(n_samples=450, noise=0.4)

    knn = KNN(k_neighbours=3)
    testing_knn(
        knn=knn,
        points=points,
        labels=labels)

    nr = nonparametric_regression(k=4, metric="l2")
    testing_nr(nr)