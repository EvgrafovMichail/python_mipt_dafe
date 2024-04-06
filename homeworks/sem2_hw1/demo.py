import numpy as np
import matplotlib.pyplot as plt
import sklearn.datasets as skd

from sci_fw.data import train_test_split
from sci_fw.enumerations import Metric
from sci_fw.algorithms import NonparametricRegressor, KNN
from sci_fw.evaluation import accuracy_ratio, MSE, MAE, determination_coef

COLORS = ("royalblue", "darkorange")


def visualize_scatter(points, labels, axis):
    unique_labes = np.unique(labels)
    for label, color in zip(unique_labes, COLORS):
        mask = labels == label
        axis.scatter(points[mask][:, 0], points[mask][:, 1], c=color)


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
axis.plot(abscissa, prediction, c=COLORS[0])
axis.scatter(abscissa, ordinate, c=COLORS[1])
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
visualize_scatter(points, labels, axis=axes[0])
axes[1].set_title(f"Predicted\nAccuracy: {acc:.3f}", fontweight="bold")
visualize_scatter(feat_train, targ_train, axis=axes[1])
visualize_scatter(feat_test, prediction, axis=axes[1])
plt.show()
