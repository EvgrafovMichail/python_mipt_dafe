import matplotlib.pyplot as plt
import numpy as np
import sklearn.datasets as skd

from metrics.metric import Metric
from visualisator.functions import (
    visualize_1d_nonparam_regres,
    visualizate_2d_weighted_KNN,
    visualize_distribution
)
from data_controler.functions import train_test_split, get_boxplot_outliers
from regressors.nonparametric_regressor import NonparametricRegressor
from regressors.weighted_KNN import WeightedKNN

POINTS_AMOUNT = 1000
BOUNDS = (-10, 10)
K_NEIGHBOURS = 100
SIGMA = 3


def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


if __name__ == '__main__':
    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = linear_modulated(abscissa)
    features_train, features_test, targets_train, targets_test = train_test_split(
        abscissa, ordinates, shuffle=True
        )
    non_param = NonparametricRegressor(k_neighbours=K_NEIGHBOURS, distance="MAE")
    non_param.fit(abscissa, ordinates)
    visualize_1d_nonparam_regres(
        features_train,
        targets_train,
        abscissa, non_param.predict(abscissa),
        non_param.predict(abscissa) - SIGMA,
        non_param.predict(abscissa) + SIGMA,
        path_to_save="Images\\NonparametricRegressionTrain.png",
    )
    visualize_1d_nonparam_regres(
        features_test,
        targets_test,
        abscissa,
        non_param.predict(abscissa),
        non_param.predict(abscissa) - SIGMA,
        non_param.predict(abscissa) + SIGMA,
        path_to_save="Images\\NonparametricRegressionTest.png",
    )

    points, labels = skd.make_multilabel_classification(
        n_samples=POINTS_AMOUNT,
        n_classes=3,
        n_features=2,
        length=1000
    )
    labels = np.sum(labels, axis=1)

    """ points, labels = skd.make_moons(n_samples=POINTS_AMOUNT, noise=0.3) """

    """ points, labels = skd.make_circles(n_samples=POINTS_AMOUNT, noise=0.3) """

    points_train, points_test, labels_train, labels_test = train_test_split(
        points, labels, shuffle=True
        )
    weighted_knn = WeightedKNN(k_neighbours=K_NEIGHBOURS)
    weighted_knn.fit(points_train, labels_train)
    visualizate_2d_weighted_KNN(
        points_train,
        weighted_knn.predict(points_train),
        path_to_save="Images\\WeightedKNNTrain.png",
    )
    visualizate_2d_weighted_KNN(
        points_test,
        weighted_knn.predict(points_test),
        path_to_save="Images\\WeightedKNNTest.png",
    )

    figure1 = plt.figure()
    figure2 = plt.figure()
    figure3 = plt.figure()

    data = np.random.normal(size=1000)
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]
    data = np.random.multivariate_normal(mean, cov, size=1000)

    visualize_distribution(figure1, data, "violin", "Images\\Violin.png")
    visualize_distribution(figure2, data, "hist", "Images\\Hist.png")
    visualize_distribution(figure3, data, "boxplot", "Images\\Boxplot.png")

    outliers = get_boxplot_outliers(data, lambda x: x)
    mask = []
    for i in range(data.shape[0]):
        if i in outliers:
            mask.append(True)
        else:
            mask.append(False)

    figure4 = plt.figure()
    figure5 = plt.figure()
    figure6 = plt.figure()

    visualize_distribution(figure4, data[mask], "violin", "Images\\Violin Outliers.png")
    visualize_distribution(figure5, data[mask], "hist", "Images\\Hist Outliers.png")
    visualize_distribution(figure6, data[mask], "boxplot", "Images\\Boxplot Outliers.png")

    plt.show()

    MeansSquaredError = Metric.get_score(targets_test, non_param.predict(features_test), "MSE")
    MeansAbsoluteError = Metric.get_score(targets_test, non_param.predict(features_test), "MAE")
    DeterminationCoef = Metric.get_score(targets_test,
                                         non_param.predict(features_test), "determination_coef")

    AccuracyOfPredicts = Metric.get_score(labels_test,
                                          weighted_knn.predict(points_test), "accuracy")

    print(
          "MeansSquaredError:",
          f"\t{MeansSquaredError}",
          "MeansAbsoluteError:",
          f"\t{MeansAbsoluteError}",
          "DeterminationCoef:",
          f"\t{DeterminationCoef}",
          "AccuracyOfPredicts:",
          f"\t{AccuracyOfPredicts}",
          sep='\n')
