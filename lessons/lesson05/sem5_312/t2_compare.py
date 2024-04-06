"""
Задача 2: сравнение слов

Вам даны 2 слова: word1 и word2
Проверьте, возможно ли из уникальных 
Букв первого слова составить второе.
"""

def is_anagram(word1: str, word2: str) -> bool:
    """ Проверка возможности составления слова word2
        из букв слова word1

        Вход:
            word1: str
                слово, из букв которого надо составить требуемое слово
            word2: str
                слово, которое требуется состваить из букв первого слова
        
        Выход:
            is_anagram: bool
                Отчёт о возможности составления нужного слова.
                True, если слово word2 можно составить 
                из уникальных букв слова word1. Иначе, False 
    """
    set1 = set(word1)
    set2 = set(word2)
    return set2.issubset(set1)


if __name__ == "__main__":
    assert is_anagram("abc", "aabc") == True
    assert is_anagram("aac", "aabc") == False
    assert is_anagram("abc", "aa") == True