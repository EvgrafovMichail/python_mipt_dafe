from datetime import datetime
from dateutil.relativedelta import relativedelta
from enum import IntEnum
from typing import Any, Iterable

from string import  (
    ascii_lowercase,
    ascii_uppercase,
    digits,
    punctuation
)


class UserFields(IntEnum):
    nickname = 0
    password = 1
    email = 2
    birthday = 3
    last_action = 4


id_gen = 1

data_base: dict[int, list[Any]] = {}
names: set[str] = set()
emails: set[str] = set()


def is_valide_nickname(nickname: str) -> bool:
    global names

    if not isinstance(nickname, str):
        raise TypeError(
                f'unexpected nickname type: {type(nickname).__name__}\n'
                'str type was expected'
        )

    nickname = nickname.casefold()

    return all([
        2 <= len(nickname) <= 10,
        nickname.isalnum(),
        not nickname[0].isdigit(),
        nickname not in names,
    ])


def is_valide_email(email: str) -> bool:
    global emails

    if not isinstance(email, str):
        raise TypeError(
                f''
        )

    return email not in emails


def is_valide_password(password: str) -> bool:
    if not isinstance(password, str):
        raise TypeError(
                f'unexpected password type: {type(password).__name__}\n'
                'str type was expected'
        )

    password_set = set(password)

    return all([
        8 <= len(password),
        password_set & set(ascii_lowercase),
        password_set & set(ascii_uppercase),
        password_set & set(digits),
        password_set & set(punctuation)
    ])


def add_user(description: list[Any]) -> None:
    global data_base, id_gen

    if not isinstance(description, list):
        raise TypeError(
                f'unexpected description type: {type(description).__name__}\n'
                'list type was expected'
        )

    if len(description) != 4:
        raise ValueError(
                f'incorrect description len: {len(description)}'
        )

    if not is_valide_nickname(description[UserFields.nickname]):
        raise ValueError()
    if not is_valide_email(description[UserFields.email]):
        raise ValueError()
    if not is_valide_password(description[UserFields.password]):
        raise ValueError()

    age = relativedelta(datetime.now(), description[UserFields.birthday])
    if age.years < 18:
        raise ValueError()


def get_users(ids: Iterable)


