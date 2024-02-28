"""
Задача 1: подсчёт количества уникальных символов в строке
"""

def unique(string: str) -> int:
    already_was=""
    unique_counter=0
    for i in string:
        if (i not in already_was):
            unique_counter+=1
            already_was+=i


    
    return unique_counter

if __name__ == "__main__":
    pass
