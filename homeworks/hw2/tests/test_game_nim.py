from nim_game.common.models import GameState, NimStateChange
from nim_game.games.game_nim import GameNim


def test_make_steps_return_value(mock_builtin_open):
    open_mock, json_load_mock = mock_builtin_open

    game = GameNim(path_to_config='')

    open_mock.assert_called_once()
    json_load_mock.assert_called_once()

    state = game.make_steps(NimStateChange(heap_id=1, decrease=1))

    assert isinstance(state, GameState)
