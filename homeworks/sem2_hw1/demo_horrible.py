class Colors:
    RED = '\033[91m'
    ENDC = '\033[0m'


if __name__ == "__main__":
    from TrainTestSplit import train_test_split
    from QualityMetrics import mse, mae, r_pow_2, accuracy
    import sklearn.datasets as skd
    from Algorithms import NPR, KNN, DistanceMetrics
    import numpy as np
    print(Colors.RED, "----NPR----", Colors.ENDC)
    test_npr = NPR(DistanceMetrics.MANHATTAN)
    values = np.arange(0, 1, 0.1).reshape(-1, 1)
    z = np.tan(values).reshape(-1, 1)
    test_npr.fit(values, z, 9)
    predicted = test_npr.predict(values)

    print(mae(z, predicted))  # честно, функции правильно написаны
    print(mse(z, predicted))  # ну мы же numpy всетаке делаем...
    print(r_pow_2(z, predicted))  # тут прикол
    print(accuracy(z, predicted))

    print(Colors.RED, "----KNN----", Colors.ENDC)
    points, labels = skd.make_moons(n_samples=200, noise=0.2)
    points_train, points_test, labels_train, labels_test = train_test_split(
        shuffle=True,
        features=points,
        targets=labels,
        train_ratio=0.8,
    )
    knn = KNN(4)
    # print(labels_train, points_train)
    knn.fit(points_train, labels_train)
    predicted = knn.predict(points_test)

    # visualize_comparison(points_test, prediction, labels_test)

    print(mae(labels_test, predicted))  # честно, функция правильно работает
    print(mse(labels_test, predicted))  # ну мы же numpy
    print(r_pow_2(labels_test, predicted))
    print(accuracy(labels_test, predicted))
