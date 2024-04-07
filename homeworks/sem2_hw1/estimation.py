import numpy as np


def mse(prediction, expectation):
    return np.sum((prediction - expectation) ** 2) / (prediction.shape[0])


def mae(prediction, expectation):
    return np.sum(abs(prediction - expectation)) / (prediction.shape[0])


def determination(prediction, expectation):
    return 1 - (np.sum((prediction - expectation) ** 2) / \
                np.sum((prediction - np.mean(prediction)) ** 2))


def accuracy(prediction, expectation):
    return np.sum(prediction == expectation)/(prediction.shape[0])


def print_estimation(prediction, expectation):
    print(f"mse = {mse(prediction, expectation)}")
    print(f"mae = {mae(prediction, expectation)}")
    print(f"R^2 = {determination(prediction, expectation)}")
    print(f"accuracy = {accuracy(prediction, expectation)}")
