very_long_string = 'this is very very very long string so long ' \
'so you need to postpone its part to the next physical line'
print(very_long_string)

another_long_string = (
    'this is very very very long string so long '
    'so you need to postpone its part to the next physical line'
)
print(another_long_string)


my_variable = 5         # валидное имя
print(f"my_variable = {my_variable}")

MyVariable = 6          # тоже валидное имя
print(f"MyVariable = {MyVariable}")

_var1 = 1               # и это валидное имя
print(f"_var1 = {_var1}")

__len__ = 4             # переопределение заразарвированной переменной
                        # так лучше никогда не делать
print(f"__len__ = {__len__}")

print("####################################################")

num1 = 5
num2 = num1
print(id(num1) == id(num2))

num1 = 6
print(id(num1) == id(num2))

id1 = id(num2)
print(f"num2 = {num2}, id = {id1}")

num2 = 3
id2 = id(num2)
print(f"num2 = {num2}, id = {id2}")

num2 = 5
id3 = id(num2)
print(f"num2 = {num2}, id = {id3}")
print(id1 == id3)


