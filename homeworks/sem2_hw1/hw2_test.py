import matplotlib.pyplot as plt
import numpy as np

from visualization.visualization import visualize_distribution
from algorithms.algorithms import get_boxplot_outliers


def draw_visualize():
    path_to_save = "/Users/kapji/Documents/MIPT/python_mipt_dafe/homeworks/sem2_hw1"
    # generating points for scatter
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]

    data = np.random.multivariate_normal(mean, cov, size=1000)

    # making axes
    figure = plt.figure(figsize=(16, 9))
    grid = plt.GridSpec(4, 4, wspace=0.2, hspace=0.2)

    axis_scatter = figure.add_subplot(grid[:-1, 1:])
    axis_hist_vert = figure.add_subplot(
        grid[:-1, 0],
        sharey=axis_scatter,
    )
    axis_hist_hor = figure.add_subplot(
        grid[-1, 1:],
        sharex=axis_scatter,
    )
    axises = [axis_scatter, axis_hist_vert, axis_hist_hor]

    visualize_distribution(axises, data, "violin", path_to_save=path_to_save)

    # 1-dim data
    data = np.random.normal(10, 10, 500)
    _, axus = plt.subplots(figsize=(16, 9))
    visualize_distribution(axus, data, "violin")


def box_outliers():
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]

    data = np.random.multivariate_normal(mean, cov, size=1000)

    abscs, ordin = get_boxplot_outliers(data, "quicksort")
    print(f"abscissa emissions: {abscs}")
    print(f"ordinates emissions: {ordin}")
