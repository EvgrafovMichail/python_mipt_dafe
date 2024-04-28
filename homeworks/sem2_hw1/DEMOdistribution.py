import numpy as np
import matplotlib.pyplot as plt
from utils.visualize import visualize_distribution


def main():
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]
    path_to_save = "C:\\Documents\\GitHub\\python_mipt_dafe\\homeworks\\sem2_hw1\\images"
    data = np.random.multivariate_normal(mean, cov, size=1000)

    figure = plt.figure(figsize=(16, 9))
    grid = plt.GridSpec(4, 4, wspace=0.2, hspace=0.2)

    axis_scatter = figure.add_subplot(grid[:-1, 1:])
    axis_hist_vert = figure.add_subplot(
        grid[:-1, 0],
        sharey=axis_scatter
    )
    axis_hist_hor = figure.add_subplot(
        grid[-1, 1:],
        sharex=axis_scatter
    )

    axises = [axis_scatter, axis_hist_vert, axis_hist_hor]

    visualize_distribution(axises, data, "violin", path_to_save=path_to_save)

    plt.show()

    # # 1-dim data
    # data = np.random.normal(10, 10, 500)
    # _, axus = plt.subplots(figsize=(16, 9))
    # visualize_distribution(axus, data, "violin")


main()
