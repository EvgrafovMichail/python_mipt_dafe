from PyQt6 import QtWidgets
from calc_ui import Ui_Form


class Window(QtWidgets.QMainWindow):

    ops = ['+', '-', '*', '/', '%']

    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.lineEdit.setReadOnly(True)
        self.ui.lineEdit.setText('0')

        self.cur = 0
        self.next = 0

        numbers = [self.ui.pushButton_0, self.ui.pushButton_1, self.ui.pushButton_2,
                   self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5,
                   self.ui.pushButton_6, self.ui.pushButton_7, self.ui.pushButton_8,
                   self.ui.pushButton_9]

        for i in range(10):
            self.connect_button(numbers[i], i)

        self.ui.pushButton_plus.clicked.connect(self.sum)
        self.ui.pushButton_eq.clicked.connect(self.eq)
        self.ui.pushButton_mul.clicked.connect(self.prod)
        self.ui.pushButton_minus.clicked.connect(self.substr)
        self.ui.pushButton_dot.clicked.connect(self.dot)
        self.ui.pushButton_percent.clicked.connect(self.mod)
        self.ui.pushButton_rev.clicked.connect(self.rev)
        self.ui.pushButton_sqr.clicked.connect(self.sqr)
        self.ui.pushButton_sqrt.clicked.connect(self.sqrt)
        self.ui.pushButton_div.clicked.connect(self.div)
        self.ui.pushButton_del.clicked.connect(self.DEL)
        self.ui.pushButton_C.clicked.connect(self.C)

    # стирание символов справа
    def DEL(self) -> None:
        text = self.ui.lineEdit.displayText()
        if len(text) == 1:
            text = '0'
        elif 'e' in text and not Window.check_for_single_operation(text):
            if len(text[:text.find('e')]) == 3:
                text = text[0] + text[text.find('e'):]
            elif len(text[:text.find('e')]) == 1:
                text = '0'
            else:
                text = text[:text.find('e')-1] + text[text.find('e'):]
        else:
            text = text[:len(text)-1]
        self.ui.lineEdit.setText(text)

    # очищение строки
    def C(self) -> None:
        self.ui.lineEdit.setText('0')

    # вычисление выражения
    def eq(self) -> None:
        text = self.ui.lineEdit.displayText()

        if Window.check_string(text):
            flag = True
            if '/' or '%' in text:
                if '/' in text:
                    if float(text[text.find('/')+1:]) == 0:
                        flag = False
                elif '%' in text:
                    if float(text[text.find('%')+1:]) == 0:
                        flag = False
            if flag:
                self.cur = eval(text)
                if int(self.cur) == self.cur:
                    self.cur = int(self.cur)
                self.next = self.cur

                self.ui.lineEdit.setText(str(self.cur))

    # вычисление числа, обратного данному
    def rev(self) -> None:
        text = self.ui.lineEdit.displayText()
        if not Window.check_for_single_operation(text):
            if float(text) != 0:
                num = 1/float(text)
                if int(num) == num:
                    num = int(num)
                text = str(num)
        self.ui.lineEdit.setText(text)

    # вычисление квадрата числа
    def sqr(self) -> None:
        text = self.ui.lineEdit.displayText()
        if not Window.check_for_single_operation(text):
            num = float(text)**2
            if (int(num) == num):
                num = int(num)
            text = str(num)
        self.ui.lineEdit.setText(text)

    # вычисление квадратного корня числа
    def sqrt(self) -> None:
        text = self.ui.lineEdit.displayText()
        if not Window.check_for_single_operation(text):
            if float(text) >= 0:
                num = float(text)**0.5
                if int(num) == num:
                    num = int(num)
                text = str(num)
        self.ui.lineEdit.setText(text)

    # знак суммы
    def sum(self) -> None:
        text = self.ui.lineEdit.displayText()

        if text[-1] not in self.ops:
            if Window.check_for_single_operation(text):
                self.eq()
            if not Window.check_for_single_operation(self.ui.lineEdit.displayText()):
                text = self.ui.lineEdit.displayText() + '+'
            self.ui.lineEdit.setText(text)

    # знак разности
    def substr(self) -> None:
        text = self.ui.lineEdit.displayText()

        if text[-1] not in self.ops:
            if Window.check_for_single_operation(text):
                self.eq()
            if not Window.check_for_single_operation(self.ui.lineEdit.displayText()):
                text = self.ui.lineEdit.displayText() + '-'
            self.ui.lineEdit.setText(text)

    # знак умножения
    def prod(self) -> None:
        text = self.ui.lineEdit.displayText()

        if text[-1] not in self.ops:
            if Window.check_for_single_operation(text):
                self.eq()
            if not Window.check_for_single_operation(self.ui.lineEdit.displayText()):
                text = self.ui.lineEdit.displayText() + '*'
            self.ui.lineEdit.setText(text)

    # знак деления с остатком
    def mod(self) -> None:
        text = self.ui.lineEdit.displayText()

        if text[-1] not in self.ops:
            if Window.check_for_single_operation(text):
                self.eq()
            if not Window.check_for_single_operation(self.ui.lineEdit.displayText()):
                text = self.ui.lineEdit.displayText() + '%'
            self.ui.lineEdit.setText(text)

    # знак деления
    def div(self) -> None:
        text = self.ui.lineEdit.displayText()

        if text[-1] not in self.ops:
            if Window.check_for_single_operation(text):
                self.eq()
            if not Window.check_for_single_operation(self.ui.lineEdit.displayText()):
                text = self.ui.lineEdit.displayText() + '/'
            self.ui.lineEdit.setText(text)

    # знак 'запятой'
    def dot(self) -> None:
        text = self.ui.lineEdit.displayText()

        if (not Window.check_for_single_operation(text)) and ('e' not in text):
            if '.' not in text:
                self.ui.lineEdit.setText(text + '.')
        else:
            for i in Window.ops:
                if ('e-' not in text and i in text and '.' not in text[text.find(i)+1:]) or \
                   ('e-' in text and i in (text[:text.find('e')] + text[text.find('e')+2:])):
                    self.ui.lineEdit.setText(text + '.')

    def connect_button(self, button: QtWidgets.QPushButton, number: int) -> None:
        button.clicked.connect(lambda: self.change_number(number))

    # изменение текущего текста
    def change_number(self, number: int) -> None:
        text = self.ui.lineEdit.displayText()

        if Window.check_for_null(text):
            text = text[:len(text)-1] + str(number)
        elif 'e' in text and (not Window.check_for_single_operation(text)):
            if '.' in text and (not Window.check_for_single_operation(text)):
                text = text[:text.find('e')] + str(number) + text[text.find('e'):]
            elif '.' not in text and (not Window.check_for_single_operation(text)):
                text = text[:text.find('e')] + '.' + str(number) + text[text.find('e'):]
        else:
            text += str(number)

        self.ui.lineEdit.setText(text)

    # проверка на то, является ли текущее число нулём
    @staticmethod
    def check_for_null(text: str) -> bool:
        if text == '0':
            return True
        elif (not Window.check_for_single_operation(text)) and '.' in text:
            return False
        elif Window.check_for_single_operation(text):
            for i in Window.ops:
                if ('e-' not in text and i in text) or \
                   ('e-' in text and i in (text[:text.find('e')] + text[text.find('e')+2:])):
                    return text[text.find(i)+1:] == '0' and ('.' not in text[text.find(i)+1:])
        return False

    # проверка на то, есть ли операция в конце строки
    @staticmethod
    def check_string(text: str) -> bool:
        if text[-1] in Window.ops or text[-1] == '.':
            return False
        return True

    # проверка на то, единственная ли операция в строке
    @staticmethod
    def check_for_single_operation(text: str) -> bool:
        sum = 0
        if text[0] == '-':
            sum -= 1
        if 'e-' in text:
            sum -= 1
        for i in Window.ops:
            sum += text.count(i)
        if sum > 1:
            raise ValueError("more than one operation in a string")
        return (sum == 1)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()

    app.exec()
