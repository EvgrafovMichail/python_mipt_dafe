from random import randint

from nim_game.common.models import NimStateChange


STONE_AMOUNT_MIN = 1        # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10       # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]      # кучки

    def __init__(self, heaps_amount: int) -> None:

        heaps_amount = int(heaps_amount)
        huh = []

        if (heaps_amount > 10) or (heaps_amount < 2):
            raise ValueError("Wrong heaps_amount value: " +
                             "should be integer between 2 and 10")

        for i in range(heaps_amount):
            stones = randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX)
            huh.append(stones)
        self._heaps = huh[:]

    def get_state(self) -> list[int]:
        return_statement = self._heaps[:]
        return return_statement

    def change_state(self, state_change: NimStateChange) -> None:

        if (state_change.heap_id < 1 or
                state_change.heap_id - 1 >= len(self._heaps)):
            raise ValueError("Inappropriate heap_id value: id should be possible to reach")

        if (state_change.decrease < 1 or
                state_change.decrease > self._heaps[state_change.heap_id - 1]):
            raise ValueError("Inappropriate decrease or state_change")

        self._heaps[state_change.heap_id - 1] -= state_change.decrease
