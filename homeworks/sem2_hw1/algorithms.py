from error_classes import ShapeMismatchError
from enum_classes import Metric
import numpy as np


def train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float,
    shuffle: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f"features' shape {features.shape[0]} != targets' shape {targets.shape}"
        )

    if train_ratio <= 0 or train_ratio >= 1:
        raise ValueError("train_ratio must be between 0 and 1")

    if shuffle:
        targets_with_features = np.hstack((targets, features[:, np.newaxis]))
        np.random.shuffle(targets_with_features)
        features, targets = targets_with_features[::, -1], targets_with_features[::, :-1]

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

    return train_targets, train_features, test_targets, test_features


def find_distances(
        to_find_points: np.ndarray,
        points: np.ndarray,
        metric: Metric,
):
    if len(to_find_points.shape) != len(points.shape):
        to_find_points = to_find_points[:, np.newaxis]

    find_points_dim = to_find_points.shape[-1]
    points = points[:, 0:find_points_dim]

    if metric == Metric.CLASSIC:
        distances = np.sqrt(np.sum((to_find_points[:, np.newaxis] - points) ** 2, axis=2))
    else:
        distances = np.abs(np.sum((to_find_points[:, np.newaxis] - points), axis=2))

    sorted_distances = np.sort(distances, axis=1)

    return (distances, sorted_distances)


def find_kernel(
        to_find_points: np.ndarray,
        points: np.ndarray,
        index_k: int,
        metric: Metric,
) -> np.ndarray:
    distances, sorted_distances = find_distances(to_find_points, points, metric)

    kernel_elem = sorted_distances[::, index_k - 1].reshape(len(sorted_distances), 1)
    kernel_argument = distances / kernel_elem
    kernel = (np.abs(kernel_argument) <= 1) * (0.75 * (1 - kernel_argument ** 2))

    return kernel


def nonparam_regression(
        to_find_points: np.ndarray,
        points: np.ndarray,
        index_k: int,
        metric: Metric,
) -> np.ndarray:
    if index_k >= len(points):
        raise ValueError(f"{index_k = } is bigger than amount of points = {len(points)}")

    if points is None or to_find_points is None:
        raise ValueError("points and to_find_points cannot be empty")

    if not (isinstance(index_k, int)):
        raise TypeError("index_k must be int")

    if not (isinstance(metric, Metric)):
        raise TypeError("metric must be Metric class")

    ordinates = points[::, 1]
    kernel = find_kernel(to_find_points, points, index_k, metric)

    numerator = np.sum(ordinates * kernel, axis=1)
    denominator = np.sum(kernel, axis=1)

    ordinates = numerator / denominator
    pred_ordinates = np.hstack((to_find_points[:, np.newaxis], ordinates[:, np.newaxis]))

    return pred_ordinates


def knn(
    to_predict_points: np.ndarray,
    points: np.ndarray,
    labels: np.ndarray,
    index_k: int,
    metric: Metric,
):
    if index_k >= len(points):
        raise ValueError(f"{index_k = } is bigger than amount of points = {len(points)}")

    if points is None or to_predict_points is None:
        raise ValueError("points and to_predict_points cannot be empty")

    if labels.shape[0] != points.shape[0]:
        raise ShapeMismatchError(
            f"labels' shape {labels.shape[0]} != points' shape {points.shape}"
        )

    if not (isinstance(index_k, int)):
        raise TypeError("index_k must be int")

    if not (isinstance(metric, Metric)):
        raise TypeError("metric must be Metric class")

    distances = find_distances(to_predict_points, points, metric)[0]
    kernel = find_kernel(to_predict_points, points, index_k, metric)
    mask = np.argsort(distances)

    labels = np.repeat(labels[np.newaxis, :], distances.shape[0], axis=0)
    sorted_labels = np.take_along_axis(labels, mask, axis=1)[:, 0:index_k]

    sorted_kernel = np.take_along_axis(kernel, mask, axis=1)[:, 0:index_k]
    labels_with_weights = np.hstack((sorted_labels, sorted_kernel))

    res_labels = np.apply_along_axis(
            lambda slice: np.bincount(
                slice[:index_k].astype(int),
                weights=slice[index_k:]).argmax(),
            arr=labels_with_weights,
            axis=1
        )

    return res_labels


def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)
    ordinates = function_values + noise
    points = np.hstack((abscissa[:, np.newaxis], ordinates[:, np.newaxis]))

    return points


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)
    ordinates = function_values + noise
    points = np.hstack((abscissa[:, np.newaxis], ordinates[:, np.newaxis]))

    return points
