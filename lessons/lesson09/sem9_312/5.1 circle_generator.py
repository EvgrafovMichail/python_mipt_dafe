""" Генератор, выдающий всю коллекцию бесконечно по кругу  """

# Напишите функцию, которая на вход получает коллекцию и возвращает
# генератор, последовательно возвращающий элементы коллекции,
# а после возврата последнего элемента коллекции последующий
# вызов генератора вернёт первый элемент коллекции, второй, и т.д.
#
# Пример:
# chars = ['a', 'b', 'c']
# generator_chars = circ_generator(chars)
# print(next(generator_chars))  # 'a'
# print(next(generator_chars))  # 'b'
# print(next(generator_chars))  # 'c'
# print(next(generator_chars))  # 'a'
# print(next(generator_chars))  # 'b'
# print(next(generator_chars))  # 'c'
# print(next(generator_chars))  # 'a'