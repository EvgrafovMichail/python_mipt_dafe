import matplotlib.pyplot as plt
import numpy as np
import sklearn.datasets as skd

from metrics.metric import Metric
from visualisator.functions import visualize_1d_nonparam_regres, visualizate_2d_weighted_KNN
from data_controler.functions import train_test_split
from regressors.nonparametric_regressor import NonparametricRegressor
from regressors.weighted_KNN import WeightedKNN

POINTS_AMOUNT = 1000
BOUNDS = (-10, 10)


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
    non_param = NonparametricRegressor()
    non_param.fit(abscissa, ordinates)
    visualize_1d_nonparam_regres(features_train, targets_train,
                                 abscissa, non_param.predict(abscissa),
                                 path_to_save="NonparametricRegressionTrian.png")
    visualize_1d_nonparam_regres(features_test, targets_test,
                                 abscissa, non_param.predict(abscissa),
                                 path_to_save="NonparametricRegressionTest.png")

    points, labels = skd.make_moons(n_samples=POINTS_AMOUNT, noise=0.3)
    points_train, points_test, labels_train, labels_test = train_test_split(
        points, labels, shuffle=True
        )
    weighted_knn = WeightedKNN()
    weighted_knn.fit(points_train, labels_train)
    visualizate_2d_weighted_KNN(points_train, weighted_knn.predict(points_train),
                                path_to_save="WeightedKNNTrain.png")
    visualizate_2d_weighted_KNN(points_test, weighted_knn.predict(points_test),
                                path_to_save="WeightedKNNTest.png")

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
