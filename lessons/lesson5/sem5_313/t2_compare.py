"""
Задача 2: сравнение слов

Вам даны 2 слова: word1 и word2
Проверьте, возможно ли из уникальных 
Букв первого слова составить второе.
"""

def is_anagram(word1: str, word2: str) -> bool:
    
    for i in word2:
        if i not in word1:
            return(False)
    return(True)


if __name__ == "__main__":
    pass