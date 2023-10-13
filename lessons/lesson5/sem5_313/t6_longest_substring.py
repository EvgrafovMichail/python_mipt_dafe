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
    stroka_now=s[0]
    max_dl=0
    for i in range(1,len(s)):
       
        if s[i] not in stroka_now:
            stroka_now+=s[i]
        else:
            max_dl=max(max_dl,len(stroka_now))
            stroka_now=stroka_now.split(s[i])
            stroka_now=stroka_now[1]+s[i]
            
    return(max(max_dl,len(stroka_now)))

print(lengthOfLongestSubstring('abcabcbb'))
# if __name__ == "__main__":
#     assert lengthOfLongestSubstring('abcabcbb') == 3
#     assert lengthOfLongestSubstring('bbbbb') == 1
#     assert lengthOfLongestSubstring('pwwkew') == 3     # 'pwke' является подпоследовательностью, 
                                                       # но не подсловом
