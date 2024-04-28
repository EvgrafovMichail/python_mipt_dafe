import os
import time
from typing import Callable
import warnings

import matplotlib.pyplot as plt
import numpy as np

from homeworks.sem2_hw1.algorithm.knn import KNN
from homeworks.sem2_hw1.algorithm.nonparam import NREGR
from metrics_distance import MAE, MSE, rr, accuracy
from precompilation import train_test_split
import sklearn.datasets as skd

from utils import (
    visualize_comparison,
    freeze_random_seed,
    Colors,
    visualize_results
)

K_NEIGHBOURS = 5
POINTS_AMOUNT = 1000
BOUNDS = (-10, 10)
FIGSIZE = (16, 8)

# подразумевается что эту функцию написал пользователь
def get_demonstration(
        function: Callable[[np.ndarray], np.ndarray],
        regressors: list[NREGR],
        path_to_save: str='',
) -> None:
    
    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = function(abscissa)

    for regressor in regressors:
        regressor.fit(abscissa, ordinates)

    _, axes = plt.subplots(1, 1, figsize=(8, 8))
    for regressor in  regressors:
        predictions = regressor.predict(abscissa)
        axes.set_title(type(regressor).__name__, fontweight='bold')
        abscissa_error = abscissa
        ordinates_error_low = ordinates - 10 # задали такую нижнюю границу коридора
        ordinates_error_up = ordinates + 10
        visualize_results(axes, abscissa, ordinates, predictions, abcissa_error=abscissa_error, ordinates_error_lower=ordinates_error_low, ordinates_error_upper=ordinates_error_up,path_to_save=path_to_save)

        print(f"MSE = {MSE(predictions, ordinates)}",
              f"MAE = {MAE(predictions, ordinates)}",
              f"rr = {rr(predictions, ordinates)}",
              sep='\n')
   
    plt.show()

# написал пользотель
def main() -> None:
    functions = [linear, linear_modulated]
    regressors = [NREGR(5, "l1")]
    pathes_to_save = ['./images/regression1.png','./images/regression2.png']
    for i, function in enumerate(functions):
        get_demonstration(function, regressors, path_to_save=pathes_to_save[i])

# написал пользотель
def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise

# написал пользотель
def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


if __name__ == '__main__':
    freeze_random_seed()
    points, labels = skd.make_moons(n_samples=400, noise=0.3)
    # visualize_scatter(points, labels)
    points_train, points_test, labels_train, labels_test = train_test_split(
        features=points,
        targets=labels,
        shuf=True,
        train_ratio=0.8,
    )
    knn = KNN(2, 'l2')
    points_train = np.array([[1,2], [2,3], [3,4], [3, 5], [4,2], [4,5], [2,4], [6,7],])
    labels_train = np.array([1,0,2, -1 , 2,7,8,9])
    points_test = np.array([[4,5], [2,4], [6,7], [5,6], [7,9], [1,2], [2,3], [3,4]])
    knn.fit(points_train, labels_train)
    prediction = knn.predict(points_test)
    
    labels_test = np.array([1,0,2, 4 ,5, 7, 9,10])
    visualize_comparison(points_test, prediction, labels_test, list(Colors), path_to_save='./images/knn.png')
    accuracy_score = accuracy(prediction, labels_test)
    
    print(f"knn accuracy: {accuracy_score}")

    time.sleep(3)

    main()
