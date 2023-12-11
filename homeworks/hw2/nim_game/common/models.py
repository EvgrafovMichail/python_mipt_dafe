from typing import Optional
from dataclasses import dataclass

from nim_game.common.enumerations import Players


# модель для описания ходов
@dataclass
class NimStateChange:
    heap_id: int                                    # номер кучки
    decrease: int                                   # количество убранных камней


# модель для описания состояния игры
@dataclass
class GameState:
    winner: Optional[Players] = None                # победитель
    opponent_step: Optional[NimStateChange] = None  # описание хода противника
    heaps_state: Optional[list[int]] = None         # состояния кучек

