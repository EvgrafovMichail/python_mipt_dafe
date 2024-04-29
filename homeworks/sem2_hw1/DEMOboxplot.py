import numpy as np
import matplotlib.pyplot as plt
from utils.random_seed import freeze_random_seed
from itertools import cycle
from Algorithms import get_boxplot_outliers
from utils.visualize import visualize_distribution


def main():
    freeze_random_seed()
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]
    data = np.random.multivariate_normal(mean, cov, size=1000).T

    figure, axis = plt.subplots(figsize=(16, 9))

    outliers = get_boxplot_outliers(data, lambda x: x)
    print(data.shape)
    print(outliers)
    print(outliers.shape)
    axis.scatter(data[0], data[1], color = 'cornflowerblue', alpha = 0.5)
    axis.scatter(data[0][outliers], data[1][outliers], color="r", alpha=0.5)
    plt.show()
    # visualize_distribution(axis, data[0][mask[0]], 'hist')


main()
