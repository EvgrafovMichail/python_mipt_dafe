from random import randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        if not isinstance(level, str) or level == "":
            raise ValueError("level must be not empty str")

        if level == "hard":
            self._level = AgentLevels.HARD
        elif level == "normal":
            self._level = AgentLevels.NORMAL
        elif level == "easy":
            self._level = AgentLevels.EASY
        else:
            raise ValueError("wrong bot difficulty")

    def easy_dif_step(self, state_curr: list[int]):
        heap_index = randint(0, len(state_curr) - 1)
        while state_curr[heap_index] == 0:
            heap_index = randint(0, len(state_curr) - 1)
        return NimStateChange(heap_index, randint(1, state_curr[heap_index]))

    def hard_dif_step(self, state_curr: list[int]):
        win_nim_sum = 0
        for i in state_curr:
            win_nim_sum ^= i

        for heap_index in range(0, len(state_curr) - 1):
            amount_of_rocks = win_nim_sum ^ state_curr[heap_index]
            change_in_rocks = state_curr[heap_index] - amount_of_rocks

            if (amount_of_rocks < state_curr[heap_index]
                    and change_in_rocks == abs(change_in_rocks)):
                return NimStateChange(heap_index, change_in_rocks)

        return self.easy_dif_step(state_curr)

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        if self._level == AgentLevels.EASY:
            return self.easy_dif_step(state_curr)

        if self._level == AgentLevels.HARD:
            return self.hard_dif_step(state_curr)

        if self._level == AgentLevels.NORMAL:
            difficulty = randint(0, 1)

            if difficulty:
                return self.hard_dif_step(state_curr)
            else:
                return self.easy_dif_step(state_curr)
