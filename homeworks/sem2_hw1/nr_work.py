import numpy as np
from nonparametric import nonparametric_regression

from accuracy import (
    MAE,
    MSE,
    get_determination
)

abscissa = np.linspace(0, 50, 200)

rand = np.random.normal(0, 5, size=abscissa.size) 
ordinates = abscissa * 3 + rand


nr = nonparametric_regression()
nr.fit(abscissa, ordinates)
predict = nr.predict(abscissa)

print(f'MAE = {MAE(predict, ordinates)}',
      f'MSE = {MSE(predict, ordinates)}',
      f'Determination = {get_determination(predict, ordinates)}')