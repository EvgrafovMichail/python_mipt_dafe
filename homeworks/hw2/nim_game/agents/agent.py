from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        level = str(level)  # level, который задается строковым литералом. level, будучи заданным строкой, может...

        if level == "easy":
            self._level = "easy"

        elif level == "normal":
            self._level = "normal"

        elif level == "hard":
            self._level = "hard"

        else:
            raise ValueError

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода

        НУЖНО ЛИ ДЕРЖАТЬ ПУСТЫЕ КУЧКИ??
        ПОПРОБУЮ
        Подразумевается, что хотя бы в одной кучке есть хотя бы один камень
        """

        def CalculateNimSum(state_curr: list[int]):
            NimSum = state_curr[0]
            for amount in state_curr[1:]:
                NimSum ^= amount
            return NimSum

        def RandomMove(state_curr: list[int]):
            while True:
                heap_id = randint(0, len(state_curr)-1)
                if state_curr[heap_id] > 0:
                    decrease = randint(1, state_curr[heap_id])
                    return NimStateChange(heap_id = heap_id, decrease = decrease)

        def OptimalMove(state_curr: list[int]):
            for heap_id in range(len(state_curr)):
                if state_curr[heap_id] < 1: # кучка не пуста
                    continue
                else:
                    for decrease in range(1, state_curr[heap_id]):
                        state_curr[heap_id] -= decrease     # Трай мува
                        if CalculateNimSum(state_curr) == 0:
                            state_curr[heap_id] += decrease # Возврат вектора к исходному значению (не уверен, что необходимо, при необходимости стереть)
                            return NimStateChange(heap_id=heap_id, decrease=decrease)
                        state_curr[heap_id] += decrease

            while True:
                heap_id = randint(0, len(state_curr))   # Ну не нашлась норм стратегия :(
                if state_curr[heap_id] > 0:
                    return NimStateChange(heap_id=heap_id, decrease=1)

        if self._level == AgentLevels.EASY:
            return RandomMove(state_curr)

        elif self._level == AgentLevels.NORMAL:
            strategy = randint(0, 1)    # Выбор стратегии
            if strategy == 1:
                return OptimalMove(state_curr)
            else:
                return RandomMove(state_curr)

        elif self._level == AgentLevels.HARD:
            return OptimalMove(state_curr)
