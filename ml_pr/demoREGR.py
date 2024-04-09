import numpy as np
from regres.Regressor import Regressor
from preprocessing import train_test_split
from metrics import mae, mse, r_score, rmse
import itertools
import matplotlib.pyplot as plt
import math



def make_regression_data(function, n_sample, noise):
    x = np.linspace(1, 10, n_sample)
    y = function(x)
    if(noise):
        y += 0.25 * np.random.normal(size=x.size)
    return x, y


"ala Grid_search )))"

def GridSearch(x, y, norms, k: np.array):
    best_score = 0
    best_params = {"norm" : "l1", "k" : 1}
    for norm , k in list(itertools.product(norms, k)):
        model = Regressor(k, norm)
        model.fit(x, y)
        y_pred = model.predict(x)
        print(f"norm = {norm} , k = {k}, mse = {mse(y_pred, y)}")
        print(f"norm = {norm} , k = {k}, mae = {mae(y_pred, y)}")
        print(f"norm = {norm} , k = {k}, r_score = {r_score(y_pred, y)}")
        print()
        if(r_score(y_pred, y) > best_score):
            best_params["norm"] = norm
            best_params["k"] = k
            best_score = r_score(y_pred, y)
    print(best_params, best_score)


def show(abscissa, ordinates, y_pred, function):

    plt.scatter(abscissa, ordinates, label='source',
                 c='royalblue', marker='o', s=1)
    plt.plot(abscissa, y_pred, label='prediction',
              c='red', linewidth=3, markersize=12,
              alpha = 0.8)
    plt.legend(["sample", "prediction"])
    plt.title(f"Regression Prediction of function {str(function.__name__)}")
    plt.show()

def linear(x):
    return 5 * x + 13

def sin(x):
    return np.sin(x)

def megazavr(x):
    return (x ** 2) * sin(x)

def main():

    norm = "l1"
    k_numbers = 100
    n_sample = 1000
    noise = True
    function = linear

    x, y = make_regression_data(function, n_sample, noise)
    
    GridSearch(x, y, ["l1", "l2"], np.arange(5, 6))

    model = Regressor(k_numbers, norm)
    model.fit(x, y)
    y_pred = model.predict(x)

    print(f"norm = {norm} , k = {k_numbers}, mse = {mse(y_pred, y)}")
    print(f"norm = {norm} , k = {k_numbers}, mae = {mae(y_pred, y)}")
    print(f"norm = {norm} , k = {k_numbers}, rmse = {rmse(y_pred, y)}")
    print(f"norm = {norm} , k = {k_numbers}, r_score = {r_score(y_pred, y)}")
    print()
    show(x, y, y_pred, function)



main()




    


