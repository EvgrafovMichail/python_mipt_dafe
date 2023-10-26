"""
Задача 6: самая длинная подстрока без повторяющихся символов

Вам дана строка s. 
Найдите длину ДЛИННЕЙШЕЙШЕГО ПОДСЛОВА, 
в котором нет повторяющихся символов


def1:
    слово w называется ПОДСЛОВОМ слова s, если
    существуют слова x и y, такие что: s = x * w * y,
    т.е. x - это префикс слова s, а y - суффикс.

def2:
    слово, состоящее только из уникальных символов,
    будем называть ОСОБЫМ.

    
Нужно найти длину самого длинного особого подслова
"""

def lengthOfLongestSubstring(s: str) -> int:
    """ Подсчёт длины самого длинного подслова
        без повторяющихся символов

        Вход:
            s : str
                исходная строка, в которой ищется особое подслово
        
        Выход:
            subs_len: int
                длина максимального особого подслова 
    """
    last_index = {}
    mx = 0

    i = 0
    while i < len(s):
        if s[i] in last_index:
            mx = max(len(last_index), mx)
            i = last_index[s[i]] + 1
            last_index = {}
            continue

        last_index[s[i]] = i
        i += 1

    return max(mx, len(last_index))


if __name__ == "__main__":
    # assert lengthOfLongestSubstring('abcabcbb') == 3
    # assert lengthOfLongestSubstring('bbbbb') == 1
    # assert lengthOfLongestSubstring('pwwkew') == 3   # 'pwke' является подпоследовательностью,
                                                       # но не подсловом
    print(lengthOfLongestSubstring('abcda'))
    print(lengthOfLongestSubstring('bbbbb'))
    print(lengthOfLongestSubstring('pwwkew'))