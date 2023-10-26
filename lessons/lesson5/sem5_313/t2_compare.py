"""
Задача 2: сравнение слов

Вам даны 2 слова: word1 и word2
Проверьте, возможно ли из уникальных
Букв первого слова составить второе.
"""

def is_anagram(word1: str, word2: str) -> bool:
    letters = {}

    if len(word1) != len(word2):
        return False

    for i in range(len(word1)):
        letter1 = word1[i]
        letters[letter1] = letters[letter1] = letters.setdefault(letter1, 0) + 1

        letter2 = word2[i]
        letters[letter2] = letters.setdefault(letter2, 0) - 1

    return all([val == 0 for val in letters.values()])

if __name__ == "__main__":
    terminal_length = 80

    print(
            '',
            'START SCRIPT'.center(terminal_length, '='),
            sep='\n'
        )
    word1 = input("Enter any first string: ")
    word2 = input("Enter any second string: ")
    print('\n' + ('Is anagram!' if is_anagram(word1, word2) else 'Is not anagram'))
    print(
            'END SCRIPT'.center(terminal_length, '='),
        )
