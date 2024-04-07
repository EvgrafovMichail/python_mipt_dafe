from tests.test_knn import test_knn
from tests.test_regression import (
    test_regression_sinus,
    test_regression_linnear
)

if __name__ == '__main__':
    test_knn()
    test_regression_sinus()
    test_regression_linnear()
