from enum import Enum


# типы игроков
class Players(Enum):
    USER = 'user'           # пользователь - человек
    BOT = 'computer'        # бот - компьютер


# уровни сложности
class AgentLevels(Enum):
    EASY = 'easy'           # простой
    NORMAL = 'normal'       # средний
    HARD = 'hard'           # сложный
