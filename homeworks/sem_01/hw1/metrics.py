from uuid import UUID
from typing import Sequence


class PeriodActiveUsers:
    def __init__(self, accumulation_period: int) -> None:
        """
        Инициализирует объект для подсчета числа уникальных пользователей.

        Args:
            accumulation_period: период времени, для которого необходимо подсчитать
                число уникальных пользователей.

        Raises:
            TypeError, если accumulation_period не может быть округлено и использовано
                для получения целого числа.
            ValueError, если после округления accumulation_period - число, меньшее 1.
        """
        # ваш код
        pass

    def add_active_users_for_curr_day(self, users: Sequence[UUID]) -> None:
        """
        Обновляет метрику на основании данных о посещении ресурса для текущего дня.

        Args:
            users: последовательность UUID пользователей, посетивших ресурс
                в данный день.
        """
        # ваш код
        pass

    @property
    def unique_users_amount(self) -> int:
        """Число уникальных пользователей за последние accumulation_period дней."""
        # ваш код
        pass

    @property
    def accumulation_period(self) -> int:
        """Период расчета метрики: accumulation_period."""
        # ваш код
        pass
