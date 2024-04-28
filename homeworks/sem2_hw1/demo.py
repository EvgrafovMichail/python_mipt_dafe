import sklearn.datasets as skd

from algorithms import (
    nonparametric_regression,
    KNN
)

from work import (
    testing_knn,
    testing_nr
)


if __name__ == '__main__':
    points, labels = skd.make_moons(n_samples=400, noise=0.3)

    knn = KNN(k_neighbours=3)
    testing_knn(
        knn=knn,
        points=points,
        labels=labels)

    nr = nonparametric_regression(k=4)
    testing_nr(nr)
