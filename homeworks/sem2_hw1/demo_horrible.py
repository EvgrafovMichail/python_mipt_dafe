class Colors:
    RED = '\033[91m'
    ENDC = '\033[0m'


def linear(x_):
    return 2 * x_ + 0.4


def make_regression_data(function_, n_sample_, noise_):
    x_ = np.linspace(1, 10, n_sample_)
    y_ = function_(x_)
    if noise_:
        y_ += np.random.normal(size=x_.size)
    return x_, y_


if __name__ == "__main__":
    from TrainTestSplit import train_test_split
    from QualityMetrics import mse, mae, r_pow_2, accuracy
    import sklearn.datasets as skd
    from Algorithms import NPR, KNN, DistanceMetrics
    import numpy as np

    print(Colors.RED, "----NPR----", Colors.ENDC)
    metric_ = DistanceMetrics.MANHATTAN
    k_numbers = 9
    n_sample = 1000
    noise = True
    function = linear

    x, y = make_regression_data(function, n_sample, noise)

    model = NPR(metric_)
    model.fit(x, y, k_numbers)
    y_pred = model.predict(x)
    for func in [mse, mae, r_pow_2]:
        print(f"{metric_=} , {k_numbers=}, {func.__name__} = {func(y_pred, y)}")

    print(Colors.RED, "----KNN----", Colors.ENDC)
    norm = DistanceMetrics.L2
    k_numbers = 8
    n_sample = 1000

    x, y = skd.make_moons(n_samples=n_sample, noise=0.6)
    knn = KNN(5, k_numbers, norm)
    x_train, x_test, y_train, y_test = train_test_split(x, y)

    knn.fit(x_train, y_train)
    y_pred = knn.predict(x_test)

    print(f"{metric_=} , {k_numbers=}, accuracy = {accuracy(y_pred, y_test)}")
