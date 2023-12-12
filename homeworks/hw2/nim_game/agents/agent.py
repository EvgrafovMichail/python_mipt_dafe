from random import choice, randint
from functools import reduce
from operator import xor

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        match level.strip().casefold():
            case 'easy':
                self._level = AgentLevels.EASY

            case 'normal':
                self._level = AgentLevels.NORMAL

            case 'hard':
                self._level = AgentLevels.HARD

            case _:
                raise ValueError(
                    "level must be 'easy', 'normal' or 'hard' "
                    f"but given {level=}"
                )

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        match self._level:
            case AgentLevels.EASY:
                return self._make_random_step(state_curr)

            case AgentLevels.NORMAL:
                next_step = choice((self._make_random_step,
                                    self._make_best_step))
                return next_step(state_curr)

            case AgentLevels.HARD:
                return self._make_best_step(state_curr)

    def _make_best_step(self, state_curr: list[int]) -> NimStateChange:
        curr_nim_sum = reduce(xor, state_curr)

        for i in range(len(state_curr)):
            heap = state_curr[i]

            if (heap ^ curr_nim_sum) < heap:
                decrease = heap - (heap ^ curr_nim_sum)
                return NimStateChange(i, decrease)

        return self._make_random_step(state_curr)

    @staticmethod
    def _make_random_step(state_curr: list[int]) -> NimStateChange:
        heap_id = randint(0, len(state_curr) - 1)
        while not state_curr[heap_id]:
            heap_id = randint(0, len(state_curr) - 1)

        decrease = randint(1, state_curr[heap_id])

        return NimStateChange(heap_id, decrease)
