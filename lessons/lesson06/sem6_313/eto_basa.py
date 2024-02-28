from datetime import datetime,timedelta
from enum import Enum
from typing import Iterable,Any
from string import ascii_letters,ascii_lowercase,digits,punctuation,ascii_uppercase



id_gen = 0

class Userfield(Enum):
    nickname = 0
    password =1
    email=2
    birthday=3
    last_action = 4

data_base={}
names:set()
emails:set()


def is_valid_nickname(nickname:str):

    global names
    if not isinstance(nickname,str):
        raise TypeError("I hate your "+type(nickname).__name__+" type")
    nickname = nickname.lower()
    if any([
        not nickname.isalnum(),
        10<len(nickname),
        2> len(nickname),
        nickname[0].isdigits(),
        nickname in names
    ]): return False
    return(True)

def is_valid_password(password:str):

    if not isinstance(password,str):
        raise TypeError("I hate your "+type(password).__name__+ " type")
    password_set = set(password)


    return any([
        8<= len(password),
        password_set & set(ascii_uppercase),
        password_set & set(ascii_lowercase),
        password_set & set(digits),
        password_set & set(punctuation),
    ])

def is_valid_birthday(birthday:datetime):
    current_year= datetime.now().year
    shifted_date = datetime(
        datetime.now().year-18,current_year.month,current_year.day    )
    return birthday <=shifted_date
def add_new_user(description:list[Any]):
    global id_gen,data_base,emails

    if not isinstance(description,list):
        raise TypeError("I hate your"+type(description).__name__+ "type")

    if len(description)!=4:
        raise ValueError("4 positions expected")

    if not is_valid_nickname(description[Userfield.nickname.value]):
        raise ValueError("инвалид nickname "+description[Userfield.nickname.value])

    if not is_valid_password(description[Userfield.password.value]):
        raise ValueError("инвалид password "+description[Userfield.password.value])

    if description[Userfield.email.value] in emails:
        raise ValueError(
            f'{description[Userfield.mail.value] }this email has already been used'
        )
    # age = datetime.now().year-description[Userfield.birthday.value].year
    # if age <=
# def get_records(ids:Iterable):
#     return("OMG bro hell nah")
#
# def change...(id,data)

def delete_record(id):
    return(666228)

def update_datetime(id,timestamp):
    return(22222222222222)







