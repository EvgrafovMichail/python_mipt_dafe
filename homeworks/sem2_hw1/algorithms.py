import sklearn.datasets as skd
import matplotlib.pylab as plt
# import scipy.stats as sps
import numpy as np

from error_classes import ShapeMismatchError
from metric_classes import Metric


def train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f"features shape {features.shape[0]} != targets shape {targets.shape}"
        )

    unique_features, unique_count = np.unique(features, return_counts=True)

    train_targets, train_features = None, None
    test_targets, test_features = None, None

    for feature_index, feature in enumerate(unique_features):
        feature_mask = features == feature
        feature_targets = targets[feature_mask]
        target_count = int(unique_count[feature_index] * train_ratio)

        if train_features is None:
            train_targets = feature_targets[:target_count]
            test_targets = feature_targets[target_count:]
            train_features = np.full(train_targets.shape[0], feature)
            test_features = np.full(test_targets.shape[0], feature)
        else:
            train_targets = np.append(train_targets, feature_targets[:target_count], axis=0)
            test_targets = np.append(test_targets, feature_targets[target_count:], axis=0)
            train_features = np.append(
                train_features,
                np.full(target_count, feature),
                axis=0
            )
            test_features = np.append(
                test_features,
                np.full(unique_count[feature_index] - target_count, feature),
                axis=0
            )

    # TODO: shuffle

    return train_targets, train_features, test_targets, test_features


# TODO: get rid of same x (distance = 0)
# TODO: proverka k
# ДЛЯ ОДНОГО Х
# def find_kernel(
#         point: np.ndarray,
#         x: int,
#         k: int,
#         metric: Metric,
# ) -> float:
#     if metric == Metric.CLASSIC:
#         distances = np.sqrt(np.sum((points[x] - points) ** 2, axis=1))
#     else:
#         distances = np.abs((point[:, np.newaxis] - point))

#     mask = distances != 0
#     distances = distances[mask]
#     print(distances)

#     sorted_distances = np.sort(distances)
#     print(sorted_distances)
#     kernel_argument = distances / sorted_distances[k - 1]

#     kernel = (np.abs(kernel_argument) <= 1) * (0.75 * (1 - kernel_argument ** 2))
#     print(kernel)
#     return kernel

#  returns predicted y(x)
# def nonparam_regression(
#         points: np.ndarray,
#         index_x,
#         index_k: int,
#         metric: Metric,
# ) -> np.ndarray:
#     abscissa, ordinates = points[::, 0], points[::, 1]
#     kernel = find_kernel(points, index_x, index_k, metric)

#     numerator = np.sum(ordinates[index_x] * kernel)
#     denominator = np.sum(kernel)
#     print(numerator)
#     print(denominator)
#     coefficients = numerator / denominator
#     pred_ordinates = coefficients * abscissa[index_x]

#     print(coefficients)
#     print(f"of: {ordinates[index_x]} pr: {pred_ordinates}")
#     return pred_ordinates

def find_kernel(
        point: np.ndarray,
        k: int,
        metric: Metric,
) -> float:
    if metric == Metric.CLASSIC:
        distances = np.sqrt(np.sum((points[:, np.newaxis] - points) ** 2, axis=2))
    else:
        distances = np.abs((point[:, np.newaxis] - point))

    # mask = distances != 0
    # distances = distances[mask].reshape(len(points), len(points) - 1)
    # print(distances)

    sorted_distances = np.sort(distances, axis=1)
    mask = sorted_distances != 0
    sorted_distances = sorted_distances[mask].reshape(len(points), len(points) - 1)
    # print(sorted_distances)
    k_element = sorted_distances[::1, k]
    # print(sorted_distances)
    k_element = k_element.reshape(len(k_element), 1)
    print(k_element)

    kernel_argument = distances / k_element

    kernel = (np.abs(kernel_argument) <= 1) * (0.75 * (1 - kernel_argument ** 2))
    kernel = kernel[~np.eye(kernel.shape[0],dtype=bool)].reshape(kernel.shape[0],-1)
    # print(kernel)
    return kernel

#  returns predicted y(x)
def nonparam_regression(
        points: np.ndarray,
        index_k: int,
        metric: Metric,
) -> np.ndarray:
    abscissa, ordinates = points[::, 0], points[::, 1]
    kernel = find_kernel(points, index_k, metric)

    # mask = np.eye(ordinates.shape[0], dtype=bool)
    ordinates = ordinates[np.newaxis,:]
    ordinates = np.repeat(ordinates, len(ordinates[0]), axis=0)
    # print(f"ord: {ordinates}")
    ordinates = ordinates[~np.eye(ordinates.shape[0],dtype=bool)].reshape(ordinates.shape[0],-1)


    numerator = np.sum(ordinates * kernel, axis=1)
    denominator = np.sum(kernel, axis=1)
    print(numerator)
    print(denominator)

    coefficients = numerator / denominator
    pred_ordinates = coefficients

    print(coefficients)
    print(f"of: {ordinates} pr: {pred_ordinates}")
    return pred_ordinates


def knn(
        
):
    pass

# seed(1)
# generate two sets of univariate observations
# data1 = 5 * np.random.randn(100) + 50
# data2 = 5 * np.random.randn(100) + 51

points, labels = skd.make_moons(n_samples=400, noise=0.3)
train_test_split(labels, points, 0.8)

points1 = np.linspace(0, 2 * np.pi, 5)
points2 = np.sin(points1)
points = np.append(points1[np.newaxis, ], points2, axis=1)
print(points)

pred_ordinates = nonparam_regression(points, 3, Metric.CLASSIC)

_, axis = plt.subplots(2, 1)
axis[0].scatter(points[:,0], points[:,1])
axis[1].scatter(points[:,0], pred_ordinates)
axis[0].plot(points[:,0], pred_ordinates)
plt.show()