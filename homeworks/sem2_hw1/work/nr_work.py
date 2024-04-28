import numpy as np

from algorithms import nonparametric_regression
from utils import (
    visualize_comparison_nparam,
    get_determination,
    MAE,
    MSE
)


abs122 = np.array([
    .12993,
    .12995,
    .14882,
    .14893,
    .15681,
    .15678,
    .17590,
    .17676,
    .19039,
    .19034,
    .19952,
    .19941,
    .21711,
    .21957,
    .23300,
    .23535
])

abs122 *= 10 ^ (-2)
ord122 = np.array([
    45,
    45,
    50,
    50,
    55,
    55,
    60,
    60,
    65,
    65,
    70,
    70,
    75,
    75,
    80,
    80
])

def testing_nr(
        nr: nonparametric_regression,
        abscissa: np.array = None,
        ordinates: np.array = None
):
    if abscissa is None or ordinates is None:
        abscissa = np.linspace(0, 50, 200)
        rand = np.random.normal(0, 5, size=abscissa.size)
        ordinates = abscissa * 3 + rand
        print("Abscissa and ordinates were created")

    abscissa = abs122
    ordinates = ord122

    nr.fit(abscissa, ordinates)
    predict = nr.predict(abscissa)

    # visualize_regression(abscissa, ordinates)
    visualize_comparison_nparam(abscissa, predict, ordinates)

    print(
        f'Mean Absolute Error = {MAE(predict, ordinates)}\n',
        f'Mean Squared Error = {MSE(predict, ordinates)}\n',
        f'Determination = {get_determination(predict, ordinates)}'
    )
