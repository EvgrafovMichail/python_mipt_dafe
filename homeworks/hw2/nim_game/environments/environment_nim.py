from random import randint

from nim_game.common.models import NimStateChange


STONE_AMOUNT_MIN = 1        # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10       # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]       # кучки

    def __init__(self, heaps_amount: int) -> None:
        self._heaps = []

        if heaps_amount < 2 or heaps_amount > 10:
            raise ValueError(
                "heaps_amount must be between 2 and 10 "
                f"but given {heaps_amount=}"
            )

        for _ in range(heaps_amount):
            self._heaps.append(
                randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX)
            )

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек

        :return: копия списка с кучек
        """
        return self._heaps[:]

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния
        """
        heap_id = state_change.heap_id
        decrease = state_change.decrease

        if heap_id < 0 or heap_id >= len(self._heaps):
            raise ValueError(f"invalid {heap_id=}")

        if decrease < 1 or decrease > self._heaps[heap_id]:
            raise ValueError(f"invalid {decrease=}")

        self._heaps[heap_id] -= decrease
