"""
Запуск игрового цикла
"""


import os

from nim_game.common.models import GameState, NimStateChange
from nim_game.games.game_nim import GameNim

from utils import print_game_state


PATH_TO_CONFIG = os.path.join('game_config.json')


def start_game_loop(path_to_config: str = PATH_TO_CONFIG) -> None:
    game_nim = GameNim(path_to_config)
    game_state = GameState(heaps_state=game_nim.heaps_state)

    print_game_state(game_state)

    while True:
        user_enter = input('enter heap id and stone amount: ')

        try:
            heap_id, decrease = tuple(map(int, user_enter.strip().split()))
            user_step = NimStateChange(heap_id=heap_id, decrease=decrease)
            game_state = game_nim.make_steps(user_step)

        except:
            print('invalid input')
            continue

        print_game_state(game_state)

        if game_state.winner is not None:
            break

