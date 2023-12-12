from unittest.mock import mock_open, MagicMock

import pytest


@pytest.fixture(scope='function')
def mock_builtin_open(mocker):
    open_mock = mock_open()
    json_load_mock = MagicMock(
        return_value={
            'heaps_amount': 5,
            'opponent_level': 'hard'
        }
    )

    mocker.patch(
        'builtins.open', open_mock
    )
    mocker.patch(
        'json.load', json_load_mock
    )

    return open_mock, json_load_mock
