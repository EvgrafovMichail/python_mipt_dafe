from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    _level: AgentLevels  # уровень сложности

    def __init__(self, level: str) -> None:
        level = AgentLevels(level)

        if level != AgentLevels.EASY and level != AgentLevels.HARD and level != AgentLevels.NORMAL:
            raise ValueError(f'{level} {type(level)}')

        self._level = level

    def _hard_move(self, state_curr: list[int]):
        # чтобы если вдруг оптимальный ход не найден, идти на 1 очко
        kolvo_elem = 1
        nim_sum = 1
        choice_state_curr_elem = 0

        for i in range(len(state_curr)):
            nim_sum = nim_sum ^ state_curr[i]

        if nim_sum == 0:
            choice_state_curr_elem = choice([i
                                             for i in range(len(state_curr))
                                             if state_curr[i] != 0
                                             ])

            kolvo_elem = randint(1, state_curr[choice_state_curr_elem])

        else:

            for i in range(len(state_curr)):  # цикл для перебора всех возможных ненулевых строк
                nim_sum = 1
                if state_curr[i] != 0:

                    for j in range(1, state_curr[i] + 1):
                        nim_sum = state_curr[i] - j
                        # цикл для вычитания значения из строки
                        for z in range(len(state_curr)):
                            # обычный перебор XOR для новой

                            if z != i:
                                nim_sum = nim_sum ^ state_curr[z]

                        if nim_sum == 0:
                            choice_state_curr_elem = i
                            kolvo_elem = j
                            break

                    if choice_state_curr_elem != 0:
                        break

        return NimStateChange(choice_state_curr_elem, kolvo_elem)

    def _easy_move(self, state_curr: list[int]):

        choice_state_curr_elem = choice([random_stuff
                                         for random_stuff in range(len(state_curr))
                                         if state_curr[random_stuff] != 0
                                         ])

        kolvo_elem = randint(1, state_curr[choice_state_curr_elem])

        return NimStateChange(choice_state_curr_elem, kolvo_elem)

    def make_step(self, state_curr: list[int]) -> NimStateChange:

        if self._level == AgentLevels.NORMAL:
            self._level = choice([AgentLevels.HARD, AgentLevels.EASY])

        if self._level == AgentLevels.EASY:
            return self._easy_move(state_curr)

        if self._level == AgentLevels.HARD:
            return self._hard_move(state_curr)
