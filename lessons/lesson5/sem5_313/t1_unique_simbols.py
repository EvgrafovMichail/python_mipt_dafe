"""
Задача 1: подсчёт количества уникальных символов в строке
"""
def unique(string: str) -> tuple[int, str]:
    """ Подсчёт количества уникальных символов в строке

        Вход:
            string: str
                исследуемая строка

        Выход:
            count: int
                количество уникальных символов в строке
    """
    unique = set(string)
    return len(unique), ','.join(unique)


if __name__ == "__main__":
    terminal_length = 80

    print(
            '',
            'START SCRIPT'.center(terminal_length, '='),
            sep='\n'
        )
    user_input = input("Enter any string: ")
    print('unique letters amount: {}\nunique letters: {}'.format(*unique(user_input)))
    print(
            'END SCRIPT'.center(terminal_length, '='),
        )
