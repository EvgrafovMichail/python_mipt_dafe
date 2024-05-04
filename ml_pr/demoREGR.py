import numpy as np
from regres.Regressor import Regressor
from metrics import mae, mse, r_score, rmse
import itertools
import matplotlib.pyplot as plt
from graphics.visualize_distribution import visualize_distribution
from graphics.regression_plot import regression_plot
from preprocessing.get_boxplot_outliers import get_boxplot_outliers


def make_regression_data(function, n_sample, noise):
    x = np.linspace(1, 10, n_sample)
    y = function(x)
    if (noise):
        y += np.random.normal(size=x.size, scale=5)
    return x, y


def GridSearch(x, y, norms, k: np.array):
    best_score = 0
    best_params = {"norm": "l1", "k": 1}
    for norm, k in list(itertools.product(norms, k)):
        model = Regressor(k, norm)
        model.fit(x, y)
        y_pred = model.predict(x)
        print(f"norm = {norm} , k = {k}, mse = {mse(y_pred, y)}")
        print(f"norm = {norm} , k = {k}, mae = {mae(y_pred, y)}")
        print(f"norm = {norm} , k = {k}, r_score = {r_score(y_pred, y)}")
        print()
        if (r_score(y_pred, y) > best_score):
            best_params["norm"] = norm
            best_params["k"] = k
            best_score = r_score(y_pred, y)
    print(best_params, best_score)
    return best_params


def show(abscissa, ordinates, y_pred, function):
    plt.figure(facecolor='#94F008')

    plt.scatter(abscissa, ordinates, label='source',
                c='blue', marker='o', s=1)
    plt.plot(abscissa, y_pred, label='prediction', c='red',
             linewidth=3, markersize=12, alpha=0.5)
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

    n_sample = 1000
    noise = True
    function = linear

    x_data, y_data = make_regression_data(function, n_sample, noise)

    mean = [2, 3]
    cov = [[1, 1], [1, 2]]
    data = np.random.multivariate_normal(mean, cov, size=1000).T

    # outliters = get_outliers(np.array([x,y]), lambda x: x)
    print(x_data.shape)
    outliters = get_boxplot_outliers(data, np.sort)

    x = data[0]
    y = data[1]
    x_out = data[0][outliters]
    y_out = data[1][outliters]

    print(x.shape, y.shape)

    best_params = GridSearch(x_data, y_data, ["l1", "l2"], np.arange(5, 6))

    k_numbers = best_params["k"]
    norm = best_params["norm"]

    model = Regressor(100, norm)
    model.fit(x_data, y_data)
    y_pred = model.predict(x_data)
    # visualize_results(x, y, y_pred)

    print(f"norm = {norm} , k = {k_numbers}, mse = {mse(y_pred, y_data)}")
    print(f"norm = {norm} , k = {k_numbers}, mae = {mae(y_pred, y_data)}")
    print(f"norm = {norm} , k = {k_numbers}, rmse = {rmse(y_pred, y_data)}")
    print(f"norm = {norm} , k ={k_numbers}, r_score={r_score(y_pred, y_data)}")
    print()

    # visualization_hw2

    visualize_distribution(np.array([x, y]), "violin",
                           "images/regression.png")
    regression_plot(np.array([x, y]), False, "images/regression.png")
    visualize_distribution(np.array([x_out, y_out]),
                           "violin", "images/regression_out1.png")

    regression_plot(np.array([x_data, y_data]), True, "images/regression.png")

    visualize_distribution(x, "boxplot",
                           "images/regression.png")

    show(x_data, y_data, y_pred, function)


main()
