# Листинги к зачету

## Содержание

- [Листинг 1](#1);  
- [Листинг 2](#2);  
- [Листинг 3](#3);  
- [Листинг 4](#4);  
- [Листинг 5](#6);  
- [Листинг 6](#6);  
- [Листинг 7](#7);  
- [Листинг 8](#8);  
- [Листинг 9](#9);  
- [Листинг 10](#10);
- [Листинг 11](#11);
- [Листинг 12](#12);
- [Листинг 13](#13);
- [Листинг 14](#14);
- [Листинг 15](#15);
- [Листинг 16](#16);
- [Листинг 17](#17);
- [Листинг 18](#18);
- [Листинг 19](#19);
- [Листинг 20](#20);
- [Листинг 21](#21);
- [Листинг 22](#22);
- [Листинг 23](#23);
- [Листинг 23](#23);
- [Листинг 24](#24);
- [Листинг 25](#25);
- [Листинг 26](#26);
- [Листинг 27](#27);
- [Листинг 28](#28);
- [Листинг 29](#29);
- [Листинг 30](#30);
- [Листинг 31](#31);
- [Листинг 32](#32);
- [Листинг 33](#33);
- [Листинг 34](#34);
- [Листинг 35](#35);


## 1

```python
my_lists = [], []
my_lists *= 2
my_lists[0].extend(i ** 2 for i in range(3))

print(my_lists)
```

[Вернуться к содержанию](#содержание)

## 2

```python
grid_size = 3

grid_1 = [[' '] * grid_size] * grid_size
grid_2 = [[' '] * grid_size for _ in range(grid_size)]

grid_1[0][0] = 'X'
grid_2[0][0] = 'X'

print(
    all(
        grid_1[i][j] == grid_2[i][j]
        for i in range(grid_size)
        for j in range(grid_size)
    )
)
```

[Вернуться к содержанию](#содержание)

## 3

```python
arr = list(range(1, 10, 2))
arr[:-2] = [2]
arr[1:1] = [145]

arr = arr[::-1] if arr else list(range(3))

print(arr)
```

[Вернуться к содержанию](#содержание)

## 4

```python
num1 = 42
num2 = 42

print(id(num1) == id(num2))

num1 = 1024
num2 = 1024

print(id(num1) == id(num2))

num1 = num2

print(id(num1) == id(num2))
```

[Вернуться к содержанию](#содержание)

## 5

```python
arr = [1, 3, 5, 4, -5, -3, -2, 3, -4, -1]
arr_sorted = arr.sort(
    key=lambda x: (abs(x), x), reverse=True
)

print(f"{arr = }", f"{arr_sorted = }", sep='\n')
```

[Вернуться к содержанию](#содержание)

## 6

```python
string = (
    'This is a real text. It has commas and dots. '
    'For example, this sentance has comma and dot.'
)

print(string.split(), end='\n\n')

delete_signs = ['.', ',']

for delete_sign in delete_signs:
    string = string.replace(delete_sign, '')

print(
    string,
    string.split(),
    sep='\n'
)
```

[Вернуться к содержанию](#содержание)

## 7
```python
words = ['CIA', 'border', 'Alabama', 'apple', 'Appel', 'zero', 'two', 'Paris']
words.sort(key=str.upper)

print(words)
```

[Вернуться к содержанию](#содержание)

## 8
```python
objects = [
    1,
    3.14,
    'string',
    set((1, 2, 3)),
    (1, 2, 3),
    (1, 2, [3]),
]

for obj in objects:
    try:
        hash_obj = hash(obj)
        print(f"object {repr(obj)} is hashable")

    except TypeError:
        print(f"object {repr(obj)} is not hashable")
```

[Вернуться к содержанию](#содержание)

## 9
```python
my_dict = {'num': 1, 'list': [1, 2, 3]}
my_dict_copy = my_dict.copy()

print(
    f'original: {my_dict};',
    f'copy: {my_dict_copy};',
    id(my_dict) == id(my_dict_copy),
    sep='\n'
)

my_dict_copy['list'].append(123)

print(
    f'original: {my_dict};',
    f'copy: {my_dict_copy};',
    sep='\n'
)
```

[Вернуться к содержанию](#содержание)

## 10
```python
dna_sequence = 'agcccaagtat'
appearances = {}

for i, nucleatide in enumerate(dna_sequence, start=1):
    appearances.setdefault(nucleatide, []).append(i)

print(appearances)
```

[Вернуться к содержанию](#содержание)

## 11

```python
my_dict = {
    str(num): num ** 2 for num in range(10)
    if num % 3 == 0 or num % 5 == 0
}

my_dict.update([(3, 30), ('5', 50)])
print(my_dict)
```
[Вернуться к содержанию](#содержание)

## 12

```python
set1 = set(range(5, 15, 2))
set2 = set(range(10))

print(set1 | set2)
print(set1 - set2)
print(set2 - set1)
print(set1 & set2)
```

[Вернуться к содержанию](#содержание)

## 13

```python
data_types = [int, float, str, list, tuple, frozenset, set]
set_of_objects = set()

for dtype in data_types:
    try:
        set_of_objects.add(dtype())

    except:
        break

else:
    print("objects of all hashable types were created")

print(set_of_objects)
```

[Вернуться к содержанию](#содержание)

## 14

```python
data_types = [int, float, str, list, tuple, frozenset, set]
set_of_objects = set()

for dtype in data_types:
    try:
        set_of_objects.add(dtype())

    except:
        continue

else:
    print("objects of all hashable types were created")

print(set_of_objects)
```
[Вернуться к содержанию](#содержание)

## 15
```python
my_dict = {}

try:
    try:
        value = my_dict['num'] / 0

    except ZeroDivisionError:
        print('handle zero division')

except KeyError:
    print('handle key error')
```
[Вернуться к содержанию](#содержание)

## 16
```python
def f():
    print('in f, before 1/0')
    1/0 
    print('in f, after 1/0')

def g():
    print('in g, before f()')
    f()
    print('in g, after f()')

def h():
    print('in h, before g()')
    try:
        g()
        print('in h, after g()')
    except ZeroDivisionError:
        print('ZD exception caught')
    print('function h ends')

h()
```
[Вернуться к содержанию](#содержание)

## 17

```python
import math

functions = {
    math.sin: math.asin, math.sinh: math.asinh,
    math.cos: math.acos, math.cosh: math.acosh
}

for key, value in list(functions.items()):
    functions[value] = key

for key, value in functions.items():
    print(f'func: {key.__name__}; inverse func: {value.__name__}')
```
[Вернуться к содержанию](#содержание)

## 18
```python
from typing import Any

def append_into_list(elem: Any, list_: list[Any] = []) -> list[Any]:    
    list_.append(elem)
    return list_

my_list = [1, 2]

print(append_into_list(1337, my_list))
print(append_into_list(42))
print(append_into_list(3.14))
```
[Вернуться к содержанию](#содержание)

## 20

```python
def f():
    var_f = 1
    def g():
        var_g = 2
        def h():
            nonlocal var_f
            var_f += var_g

        h()
    g()
    
    print(f'{var_f = }')

f()
```
[Вернуться к содержанию](#содержание)

## 21

```python
some_number = 9


def func1(num: int) -> None:
    print(f'{num = };')
    print(f'{some_number = };')
    print('')


def func2(num: int) -> None:
    some_number = 6
    print(f'{num = };')
    print(f'{some_number = };')
    print('')


def func3(num: int) -> None:
    print(f'{num = };')
    print(f'{some_number = };')
    some_number = 6
    print('')

func1(3)
func2(3)
func3(3)
```
[Вернуться к содержанию](#содержание)

## 22

```python
def func3(num: int) -> None:
    global some_number

    print(f'{num = };')
    print(f'{some_number = };')
    some_number = 6
    print('')

func3(3)

print(f'{some_number = };')
```
[Вернуться к содержанию](#содержание)

## 23

```python
from typing import Callable


def outer_func(num: int) -> Callable:
    outer_num = num

    def inner_func(num: int) -> None:
        print(f'inner_{num = };')
        print(f'{outer_num = };')
        outer_num = 5
        print('')

    print(f'{outer_num = };')

    return inner_func

inner_func = outer_func(10)
inner_func(3)
```
[Вернуться к содержанию](#содержание)

## 24

```python
counter = 0


def count() -> int:
    global counter
    
    counter += 1
    return counter

counter1 = count
counter2 = count

print(counter1())
print(counter2())
```
[Вернуться к содержанию](#содержание)

## 25

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print('start function')
        result = func(*args, **kwargs)
        print('finished function')

        return result
    
    return wrapper


@my_decorator
def do_something():
    print('do_something')

do_something()
```
[Вернуться к содержанию](#содержание)

## 26

```python
def decorate(func):
    print('run decorate')
    return func


@decorate
def do_something() -> None:
    print('do_something')


@decorate
def do_another_thing() -> None:
    print('do_another_thing')
```
[Вернуться к содержанию](#содержание)

## 27

```python
def outer(func):
    def wrapper(*args, **kwargs):
        print('outer')
        
        result = func(*args, **kwargs)
        return result
    
    return wrapper


def inner(func):
    def wrapper(*args, **kwargs):
        print('inner')

        result = func(*args, **kwargs)
        return result
    
    return wrapper


@outer
@inner
def do_something() -> None:
    print('do_something')

do_something()
```
[Вернуться к содержанию](#содержание)

## 28

```python
words = [
    'apple', 'grass', 'station', 'begin', 'orange',
    'sin', 'glass', 'storage', 'vibration', 'formation'
]

words_sorted = sorted(words, key=lambda x: x[::-1])

print(words_sorted)
```
[Вернуться к содержанию](#содержание)

## 29

```python
from typing import Generator


def generate_even_digits() -> Generator:
    num_curr = 0

    while True:
        if num_curr >= 10:
            return 'numbers are exhausted'
        
        if num_curr % 2 == 0:
            yield num_curr

        num_curr += 1

generator = generate_even_digits()

print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
```
[Вернуться к содержанию](#содержание)

## 30

```python
from typing import Generator


def generate_pyramid_sequence(top_number: int) -> Generator:
    if top_number <= 1:
        raise ValueError('top number should be greater than 1')
    
    top_number = int(top_number)
    
    yield from range(1, top_number)
    yield from range(top_number, 0, -1)

for i in generate_pyramid_sequence(5):
    print(i, end=' ')
```
[Вернуться к содержанию](#содержание)

## 31

```python
limit = 19

list1 = [i for i in range(limit) if i % 3 == 0]
list2 = [i for i in range(limit) if i % 2 == 0]

list_zipped_once = list(zip(list1, list2))
list_zipped_twice = list(zip(*list_zipped_once))

list_mapped = list(map(lambda x, y: x + y, *list_zipped_twice))

print(list_zipped_twice, list_mapped, sep='\n')
```
[Вернуться к содержанию](#содержание)

## 32
```python
class MyClass:
    def print_hello(self) -> None:
        print("Hello!")

    @staticmethod
    def print_main_answer() -> None:
        print("Main answer is 42!")

my_class = MyClass()

my_class.print_hello()
my_class.print_main_answer()

my_class.answer = 42

print(my_class.answer)
print(MyClass.answer)
```
[Вернуться к содержанию](#содержание)

## 33
```python
class MyClass:
    def print_hello(self) -> None:
        print("Hello!")

    @staticmethod
    def print_main_answer() -> None:
        print("Main answer is 42!")

my_class = MyClass()

my_class.print_hello()
my_class.print_main_answer()

MyClass.answer = 42

print(my_class.answer)
print(MyClass.answer)
```
[Вернуться к содержанию](#содержание)

## 34

```python
class Parallelogram:
    def area(self) -> None:
        print('parallelogram area')


class Rectangle(Parallelogram):
    def area(self) -> None:
        print('rectangle area')


class Rhombus(Parallelogram):
    def area(self) -> None:
        print('rhombus area')


class Square(Rectangle, Rhombus):
    pass

square = Square()
square.area()
```
[Вернуться к содержанию](#содержание)

## 35

```python
class Parent:
    def __init__(self) -> None:
        print('init Parent')


class ChildWrong(Parent):
    def __init__(self) -> None:
        print('init ChildWrong')


class ChaildNaive(Parent):
    pass


class ChildGood(Parent):
    def __init__(self) -> None:
        super().__init__()
        print('init ChildGood')

child_wrong = ChildWrong()
child_naive = ChaildNaive()
child_good = ChildGood()
```
[Вернуться к содержанию](#содержание)
