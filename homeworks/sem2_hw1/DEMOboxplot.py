import numpy as np
import matplotlib.pyplot as plt
from utils.random_seed import freeze_random_seed
from Algorithms import get_boxplot_outliers

def main():
    freeze_random_seed()
    mean = [2, 3]
    cov = [[1, 1], [1, 2]]
    data = np.random.multivariate_normal(mean, cov, size=1000)

    figure = plt.figure(figsize=(16, 9))

main()
