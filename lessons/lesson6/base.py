from datetime import datetime
from string import punctuation


class User:
    def __init__(self, nickname, mail, birth, password) -> None:
        self.nickname = nickname
        self.mail = mail
        self.birth = birth
        self.password = password
        self.last_action = datetime.today().strftime('%Y-%m-%d')

    def update_action(self):
        self.last_action = datetime.today().strftime('%Y-%m-%d')
    
    def get_info(self):
        self.update_action()

        print(f'Nickname = {self.nickname} \n' \
                f'Mail = {self.mail} \n'\
                f'Birth = {self.birth} \n' \ 
                f'Last action = {self.last_action}')


class DataBase:
    def __init__(self) -> None:
        self.data = []
        self.nickname = set()
        self.mails = set()
    def check_nickname(self, nickname: str):
        if nickname in self.nickname:
            raise ValueError("not uniq")
        
        if not (2 <= len(nickname) <= 10): 
            raise ValueError('wrong size')
        if nickname[0].isdigit() or not (nickname.isalnum() and nickname.isascii()):
            raise ValueError('unvalid user')                

    def check_password(self, password):
        if len(password) < 8:
            raise ValueError('Too short password')      
        upper = False
        digit = False
        lower = False
        punct = False
        for elem in password:
            if elem.isascii():
                if elem.isapper():
                    upper = True

                elif elem.islower():
                    lower = True

                elif elem.isdigit():
                    digit = True
                
                elif elem in punctuation:
                    punct = True
                else:
                    raise ValueError('invalid password')
            else:
                raise ValueError('invalid password')

        if not (upper and digit and lower and punct):
            raise ValueError('invalid password')     
    def check_mail(self, mail):
        if mail[-13:] != '@phystech.edu':
            raise ValueError('MAI detection') #invalid user

        if mail.count("@") != 1:
            raise ValueError('invalid mail')
        if mail in self.mails:
            return ValueError('mail is already used')

    def chech_birth(self, birth):
        today = datetime.today().strftime('%Y-%m-%d')

        if (today -birth) / 365 < 18:
            raise ValueError('too young')
    def add_user(self, nickname, password, mail, birth):
        birth = datetime.strptime(birth, '%Y-%m-%d').date()
        self.check_nickname(nickname)
        self.chech_birth(birth)
        self.check_mail(mail)
        self.check_password(password)

        self.mails.add(mail)
        self.nickname.add(nickname)

        self.data.append(User(nickname, password, mail, birth))       
        
    def del_user(self):
        pass

    def user_info(self):
        pass

    def change_data(self):
        pass

    def update(self):
        pass