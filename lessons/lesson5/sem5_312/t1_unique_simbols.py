"""
Задача 1: подсчёт количества уникальных символов в строке
"""

def unique(string: str) -> int:
    """ Подсчёт количества уникальных символов в строке

        Вход:
            string: str
                исследуемая строка
        
        Выход:
            count: int
                количество уникальных символов в строке
    """
    return len(set(string))

if __name__ == "__main__":
    assert unique("мама") == 2
    assert unique("qwerty") == 6
    assert unique("aaa") == 1

