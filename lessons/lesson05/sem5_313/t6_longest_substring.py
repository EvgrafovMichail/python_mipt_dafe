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
    i = j = 1 # Смотрим на подстроку от s[i] до s[j]
    mx = 0 # самое длинное слово
    while j!= len(s):
        if len( s[i:j] ) == len( { s[i:j] } ):
            mx = max(mx, j-i)
            j += 1
        else: 
            i += 1
    return mx

if __name__ == "__main__":
    assert lengthOfLongestSubstring('abcabcbb') == 3
    assert lengthOfLongestSubstring('bbbbb') == 1
    assert lengthOfLongestSubstring('pwwkew') == 3     # 'pwke' является подпоследовательностью, 
                                                       # но не подсловом
