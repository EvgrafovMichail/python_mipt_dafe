import pytest
import numpy as np

from data_controler.exceptions import ShapeMismatchError
from data_controler.functions import train_test_split

AMOUNT_OBJ = 10
TRAIN_RATIO = 0.6


def test_init_raise_exception():
    with pytest.raises(ShapeMismatchError):
        train_test_split(np.arange(AMOUNT_OBJ), np.arange(AMOUNT_OBJ - 1))
    with pytest.raises(ValueError):
        train_test_split(np.arange(AMOUNT_OBJ),
                         np.arange(AMOUNT_OBJ), train_ratio=3)


def test_working():
    features = np.arange(AMOUNT_OBJ)
    targets = np.arange(AMOUNT_OBJ)

    features_train, features_test, targets_train, targets_test = train_test_split(
        features, targets
        )
    assert np.all(features_train == targets_train)
    assert np.all(features_test == targets_test)


def test_separation():
    features = np.arange(AMOUNT_OBJ)
    targets = np.arange(AMOUNT_OBJ)

    features_train, features_test, targets_train, targets_test = train_test_split(
        features, targets, train_ratio=TRAIN_RATIO
        )
    assert features_train.shape[0] == targets_train.shape[0] == AMOUNT_OBJ * TRAIN_RATIO
    assert features_test.shape[0] == targets_test.shape[0] == AMOUNT_OBJ * (1 - TRAIN_RATIO)


def test_shuffle():
    features = np.arange(AMOUNT_OBJ)
    targets = np.arange(AMOUNT_OBJ)

    features_train, features_test, targets_train, targets_test = train_test_split(
        features, targets, shuffle=True
        )
    assert np.all(features_train == targets_train)
    assert np.all(features_test == targets_test)

    features = np.arange(AMOUNT_OBJ)
    targets = np.mod(np.arange(AMOUNT_OBJ), 3)

    features_train, features_test, targets_train, targets_test = train_test_split(
        features, targets, shuffle=True, classification=True
        )
    assert np.all(np.mod(features_train, 3) == targets_train)
    assert np.all(np.mod(features_test, 3) == targets_test)
