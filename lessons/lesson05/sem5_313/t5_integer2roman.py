
def intToRoman(num: int) -> str:
    if num > 9999: 
        return ""
    ones = "IXCM"
    fives = "VLD"
    result = ""
    num = str(num)
    while num:
        rims = ""
        symbol = num[0]
        k = len(num) - 1
        if int(symbol) == 0:
            num = num[1:]
            continue
        if symbol == "4":
            rims = ones[k] + fives[k]
        elif symbol == "9":
            rims = ones[k] + (ones[k + 1])
        else:
            if int(symbol) >= 5:
                rims = fives[k] 
            rims += ones[k] * (int(symbol) % 5)
        num = num[1:]
        result += rims
    return result

def lengthOfLongestSubstring(s: str) -> int:
    result = 0
    i = j = 0
    while (j < len(s)):
        if len(s[i:j+1]) == len( set(s[i:j+1]) ):
            result = max(len(s[i:j+1]), result)
            j += 1
        else:
            i += 1
    return result