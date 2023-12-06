"""
Просто CLI
"""


from nim_game.common.models import GameState


def print_game_state(game_state: GameState) -> None:
    if game_state.opponent_step:
        print(
            f'Bot removed {game_state.opponent_step.decrease} stones'
            f' from {game_state.opponent_step.heap_id} heap;'
        )

    if game_state.heaps_state:
        print('heaps:\n')

        for i, stones_amount in enumerate(game_state.heaps_state, start=1):
            print(f'heap_{i}: {"■" * stones_amount}')

    if game_state.winner:
        print(f'game finished; {game_state.winner.value} won;')
