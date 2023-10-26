from unittest.mock import mock_open

import pytest


@pytest.fixture(scope='function')
def mock_builtin_open(mocker):
    open_mock = mock_open()

    mocker.patch(
        'builtins.open', open_mock
    )

    return open_mock
