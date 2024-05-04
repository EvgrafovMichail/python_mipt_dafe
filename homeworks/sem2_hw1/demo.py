import numpy as np
import matplotlib.pyplot as plt
import sklearn.datasets as skd

from sci_fw.data import train_test_split
from sci_fw.enumerations import Metric, PlotType
from sci_fw.algorithms import NonparametricRegressor, KNN
from sci_fw.evaluation import accuracy_ratio, MSE, MAE, determination_coef
from sci_fw.visualization import (
    visualize_distribution, visualize_classification, visualize_regression, get_boxplot_outliers
)


# Distribution

def plot_distribution(
    data: np.ndarray,
    plot_type: PlotType,
    suptitle: str
) -> None:
    figure = plt.figure(figsize=(8, 8))
    figure.suptitle(suptitle, fontweight="bold")
    grid = plt.GridSpec(4, 4, wspace=.2, hspace=.2)

    axis_scatter = figure.add_subplot(grid[:-1, 1:])
    axis_hist_vert = figure.add_subplot(
        grid[:-1, 0],
        sharey=axis_scatter,
    )
    axis_hist_hor = figure.add_subplot(
        grid[-1, 1:],
        sharex=axis_scatter,
    )

    axes = [axis_scatter, axis_hist_vert, axis_hist_hor]
    axes[1].invert_xaxis()
    axes[2].invert_yaxis()
    visualize_distribution(axes, data, plot_type, "")
    plt.show()


mean = [2, 3]
cov = [[1, 1], [1, 2]]
abscissa, ordinates = np.random.multivariate_normal(mean, cov, size=1000).T
data = np.vstack((abscissa, ordinates)).T

for plot_type in list(PlotType):
    plot_distribution(data, plot_type, f"{plot_type.value} distribution example")

outliers_x = get_boxplot_outliers(data, lambda arr: arr[0])
outliers_y = get_boxplot_outliers(data, lambda arr: arr[1])
outliers = np.unique(np.hstack((outliers_x, outliers_y)))
outliers = data[outliers]
plot_distribution(outliers, PlotType.HIST, "boxplot outliers example")

_, axes = plt.subplots(figsize=(8, 8))
axes.set_title("1d distribution example", fontweight="bold")
visualize_distribution(axes, abscissa, PlotType.HIST)
plt.show()


# Nonparametric regressor
abscissa = np.linspace(-10, 10, 1000)
ordinate = np.sin(abscissa) * abscissa
ordinate += np.random.normal(size=abscissa.size)
reg = NonparametricRegressor(75, metric="l1")
reg.fit(abscissa, ordinate)
prediction = reg.predict(abscissa)

mse = MSE(ordinate, prediction)
mae = MAE(ordinate, prediction)
r2 = determination_coef(ordinate, prediction)

figure, axis = plt.subplots(figsize=(16, 8))
axis.set_title(
    f"Nonparametic regression\nMSE: {mse:.3f} MAE: {mae:.3f} R^2: {r2:.3f}",
    fontweight="bold")
points = np.vstack((abscissa, ordinate)).T
prediction = np.vstack((abscissa, prediction)).T
error = np.ones(abscissa.shape)
visualize_regression(axis, points, prediction, error)
plt.show()

# KNN
points, labels = skd.make_moons(n_samples=400, noise=0.3)
knn = KNN(5, metric=Metric.EUCLIDEAN)
feat_train, feat_test, targ_train, targ_test = train_test_split(points, labels)
knn.fit(feat_train, targ_train)
prediction = knn.predict(feat_test)

acc = accuracy_ratio(prediction, targ_test)

_, axes = plt.subplots(ncols=2, figsize=(16, 8))
axes[0].set_title("Actual", fontweight="bold")
visualize_classification(axes[0], points, labels)
axes[1].set_title(f"Predicted\nAccuracy: {acc:.3f}", fontweight="bold")
visualize_classification(axes[1], feat_train, targ_train)
visualize_classification(axes[1], feat_test, prediction)
plt.show()

# Classification
features = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
labels = [1, 2, 3, 4, 3]
colors = ("r", "g", "b")
_, axes = plt.subplots(figsize=(8, 8))
axes.set_title(f"Classification example\n{colors=}", fontweight="bold")
visualize_classification(axes, features, labels, colors)
for feat, label in zip(features, labels):
    axes.annotate(f"Label {label}", (feat[0]-.17, feat[1]+.05))
plt.show()
