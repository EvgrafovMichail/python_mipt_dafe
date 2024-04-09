import numpy as np
import matplotlib.pyplot as plt

from algorithms import nonparametric_regression
from utils import(
    visualize_comparison_nparam,
    visualize_regression,
    get_determination,
    MAE,
    MSE
)

abscissa = np.linspace(0, 50, 200)
rand = np.random.normal(0, 5, size=abscissa.size) 
ordinates = abscissa * 3 + rand

def testing_nr(
        nr: nonparametric_regression,
        abscissa: np.array = abscissa,
        ordinates: np.array = ordinates
):
    nr.fit(abscissa, ordinates)
    predict = nr.predict(abscissa)

    #Svisualize_regression(abscissa, ordinates)
    visualize_comparison_nparam(abscissa, predict, ordinates)

    print(
        f'Mean Absolute Error = {MAE(predict, ordinates)}\n',
        f'Mean Squared Error = {MSE(predict, ordinates)}\n',
        f'Determination = {get_determination(predict, ordinates)}'
    )
