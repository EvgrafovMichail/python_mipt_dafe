"""
Задача 6: самая длинная подстрока без повторяющихся символов

Вам дана строка s. 
Найдите длину ДЛИННЕЙШЕЙШЕГО ПОДСЛОВА, 
в котором нет повторяющихся символов


def1:
    слово w называется ПОДСЛОВОМ слова s, если
    существуют слова x и y, такие что: s = x + w + y,
    т.е. x - это префикс слова s, а y - суффикс.

def2:
    слово, состоящее только из уникальных символов,
    будем называть ОСОБЫМ.

    
Нужно найти длину самого длинного особого подслова
"""

def lengthOfLongestSubstring(s: str) -> int:
    if len(set(s)) == 1:
        return 1
    elif len(set(s)) == len(s):
        return len(s)
    
    l = []
    max_lenght = 1
    for symbol in s:
        if symbol not in l:
            l.append(symbol)
            max_lenght = max(len(l), max_lenght)
        else:
            while l[0] != symbol:
                l.pop(0)
            l.pop(0)
            l.append(symbol)
            max_lenght = max(len(l), max_lenght)
    return max_lenght


if __name__ == "__main__":
    assert lengthOfLongestSubstring('abcabcbb') == 3
    assert lengthOfLongestSubstring('bbbbb') == 1
    assert lengthOfLongestSubstring('bcdefg') == 6
    assert lengthOfLongestSubstring('asdfghdjefhkss') == 7
    assert lengthOfLongestSubstring('pwwkew') == 3     # 'pwke' является подпоследовательностью, 
                                                       # но не подсловом