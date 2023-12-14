from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """
    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        if level == 'hard' \
            or level == 'normal' \
                or level == 'easy':
            self._level = AgentLevels(level)
        else:
            raise ValueError()

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности
        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        Подразумевается, что хотя бы в одной кучке есть хотя бы один камень
        """
        if self._level == AgentLevels.EASY:
            return Agent._random_move(state_curr)

        elif self._level == AgentLevels.NORMAL:
            if randint(0, 1):
                return Agent._optimal_move(state_curr)
            return Agent._random_move(state_curr)

        elif self._level == AgentLevels.HARD:
            return Agent._optimal_move(state_curr)

    @staticmethod
    def _calculate_nim_sum(state_curr: list[int]) -> int:  # Вычисляет ним-сумму
        nim_sum = state_curr[0]  # теоретически оптимизированнее, чем задавать 0 и считать
        for amount in state_curr[1:]:
            nim_sum ^= amount
        return nim_sum  # вот бы была операция, как sum() для такого

    @staticmethod
    def _random_move(state_curr: list[int]) -> NimStateChange:
        heap_id = choice([i for i in range(len(state_curr)) if state_curr[i]])
        decrease = randint(1, state_curr[heap_id])
        return NimStateChange(heap_id=heap_id, decrease=decrease)

    @staticmethod
    def _optimal_move(state_curr: list[int]) -> NimStateChange:
        for heap_id in range(len(state_curr)):
            if state_curr[heap_id] < 1:     # Можно поставить равенство 0
                continue
            for decrease in range(1, state_curr[heap_id]):
                state_curr[heap_id] -= decrease     # Трай мува
                if Agent._calculate_nim_sum(state_curr=state_curr) == 0:
                    return NimStateChange(heap_id=heap_id, decrease=decrease)
                state_curr[heap_id] += decrease     # мув найдется гарантированно

        return NimStateChange(  # 1 камень из случайной кучки, как сказал Евграфов
            heap_id=choice([i for i in range(len(state_curr)) if state_curr[i]]),
            decrease=1)
