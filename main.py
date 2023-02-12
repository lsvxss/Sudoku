import sys
import sqlite3
import random
from PyQt5 import uic
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog
from PyQt5.QtCore import Qt

"""Основной класс для игры в Судоку"""


class Sudoku(QMainWindow):
    """При инициализации отображает главное окно программы,
     получает в аргументах id пользователя, его имя, а также
      обрабатывает все события происходящие в главном окне
      (нажатие кнопок и взаимодействие с меню)."""
    def __init__(self, id, name):
        super(Sudoku, self).__init__()
        uic.loadUi('main.ui', self)  # подключение к ui-файлу главного окна
        self.point_light_level = 0
        self.point_middle_level = 0
        self.point_high_level = 0  # 3 данных переменных необходимы для
        # того, чтобы определять, сколько начислять баллов пользователю
        # в зависимости от выбранного им уровня
        self.name = name  # присвоение имени пользователя в переменную класса
        self.id = id  # присвоение id пользователя в переменную класса
        self.setWindowIcon(QIcon("sudoku.png"))  # добавление иконки в окно приложения
        self.action_3.triggered.connect(self.show_my_progress)  # подключение к методу
        # show_my_progress при нажатии на action_3
        self.action.triggered.connect(self.info)  # подключение к методу
        # info при нажатии на action
        self.pushButton.clicked.connect(self.light_level)  # подключение к методу
        # light_level при нажатии на кнопку pushButton
        self.pushButton_2.clicked.connect(self.middle_level)  # подключение к методу
        # middle_level при нажатии на кнопку pushButton_2
        self.pushButton_3.clicked.connect(self.high_level)  # подключение к методу
        # high_level при нажатии на кнопку pushButton_3
        self.pushButton_4.clicked.connect(self.back_dialog)

    """Метод возврата к прошлому окну"""

    def back_dialog(self):
        self.hide()
        self.second_form = Dialog()
        self.second_form.show()

    """Метод легкого уровня игры.
        В нем идет подключение к ui-файлу game.ui игры, QLineEdit'ы 
        (то есть сами клетки игры) заполняются заданными в словаре значениями"""

    def light_level(self):  # метод для игры в судоку на лёгком уровне
        uic.loadUi('game.ui', self)  # подключение к ui-файлу игры
        self.setWindowIcon(QIcon("sudoku.png"))
        # добавление иконки в окно приложения
        self.point_light_level = 1
        for i in range(1, 82):
            obj_label = getattr(self, "lineEdit_{}".format(i))
            # возвращает значение атрибута указанного объекта по его имени
            font = QFont()
            font.setPointSize(20)  # установление размера текста в QLineEdit
            obj_label.setFont(font)
            obj_label.setAlignment(Qt.AlignCenter)
            # установка текста по центру
        self.dict = {2: '6', 3: '5', 4: '2', 5: '4', 6: '3', 8: '9', 9: '1',
                     10: '7', 12: '4', 13: '5', 16: '3', 17: '8', 18: '6',
                     19: '9', 20: '3', 21: '1', 29: '2', 31: '1', 34: '3',
                     37: '1', 39: '8', 40: '9', 43: '6', 44: '5', 45: '2',
                     48: '4', 49: '7', 51: '2', 52: '8', 54: '9', 56: '8',
                     60: '7', 62: '1', 71: '6', 73: '4', 79: '5', 80: '8',
                     81: '3'}  # словарь, где ключами являются номера виджетов
        # QLineEdit, а значения - числа, которые кладутся в клетки судоку
        for i in self.dict.keys():  # в данном цикле идет заполнение клеток
            # судоку числами из словаря
            obj_label = getattr(self, "lineEdit_{}".format(i))
            obj_label.setText(self.dict[i])
            obj_label.setEnabled(False)  # создание защищенного поля вывода
            obj_label.setAlignment(Qt.AlignCenter)  # расположение текста по центру
        self.pushButton.clicked.connect(self.check)  # подключение к методу check
        # при нажатии на кнопку
        self.pushButton_2.clicked.connect(self.back)  # подключение к методу back
        # при нажатии на кнопку
        self.pushButton_3.clicked.connect(self.use_hint)  # подключение к методу use_hint
        # при нажатии на кнопку

    """Метод проверки верности решения Судоку.
    Идет проверка верного выполнения игры - проверяются столбцы,
    строки и квадраты игрового поля. При неверном заполнении клеток в 
    label помещается сообщение об ошибке."""

    def check(self):  # метод проверки заполнения судоку
        list_of_cols_1 = [1, 4, 7, 28, 31, 34, 55, 58, 61]
        list_of_cols_2 = [10, 13, 16, 37, 40, 43, 64, 67, 70]
        list_of_cols_3 = [19, 22, 25, 46, 49, 52, 73, 76, 79]
        # списки номеров клеток для проверки верности выполнения Судоку
        # по столбцам
        list_of_rows_1 = [1, 2, 3, 10, 11, 12, 19, 20, 21]
        list_of_rows_2 = [28, 29, 30, 37, 38, 39, 46, 47, 48]
        list_of_rows_3 = [55, 56, 57, 64, 65, 66, 73, 74, 75]
        # списки номеров клеток для проверки верности выполнения Судоку
        # по строкам
        list_of_squares = [[1, 10], [10, 19], [19, 28], [28, 37],
                           [37, 46], [46, 55], [55, 64], [64, 73],
                           [73, 82]]
        # список номеров клеток для проверки верности выполнения Судоку
        # по квадратам
        check_list_of_cols = []
        check_list_of_rows = []
        check_list_of_squares = []
        count = 0  # переменная-счётчик, которая улавливает ошибки в судоку
        count_2 = 0
        # проверка заполнения клеток игры, что в них текст является числом
        # от 1 до 9
        for i in range(1, 82):
            obj_label = getattr(self, "lineEdit_{}".format(i))
            if obj_label.text().isdigit():
                if 1 <= int(obj_label.text()) <= 9:
                    count_2 += 1
        if count_2 == 81:
            """В следующих 3 циклах идет проверка на правильное заполнение 
            столбцов в судоку"""
            for i in range(0, 3):
                check_list_of_cols.clear()
                for j in list_of_cols_1:
                    obj_label = getattr(self, "lineEdit_{}".format(j + i))
                    if 1 <= int(obj_label.text()) <= 9:
                        check_list_of_cols.append(int(obj_label.text()))
                    else:
                        self.label.setText('Найден неверный символ!')
                if len(set(check_list_of_cols)) != len(check_list_of_cols):
                    count += 1
            check_list_of_cols.clear()
            for i in range(0, 3):
                check_list_of_cols.clear()
                for j in list_of_cols_2:
                    obj_label = getattr(self, "lineEdit_{}".format(j + i))
                    if 1 <= int(obj_label.text()) <= 9:
                        check_list_of_cols.append(int(obj_label.text()))
                    else:
                        self.label.setText('Найден неверный символ!')
                if len(set(check_list_of_cols)) != len(check_list_of_cols):
                    count += 1
            check_list_of_cols.clear()
            for i in range(0, 3):
                check_list_of_cols.clear()
                for j in list_of_cols_3:
                    obj_label = getattr(self, "lineEdit_{}".format(j + i))
                    if 1 <= int(obj_label.text()) <= 9:
                        check_list_of_cols.append(int(obj_label.text()))
                    else:
                        self.label.setText('Найден неверный символ!')
                if len(set(check_list_of_cols)) != len(check_list_of_cols):
                    count += 1
            """В следующих 3 циклах идет проверка на правильное заполнение 
                    строк в судоку"""
            for i in range(0, 3):
                check_list_of_rows.clear()
                for j in list_of_rows_1:
                    obj_label = getattr(self, "lineEdit_{}".format(j + 3 * i))
                    if 1 <= int(obj_label.text()) <= 9:
                        check_list_of_rows.append(int(obj_label.text()))
                    else:
                        self.label.setText('Найден неверный символ!')
                if len(set(check_list_of_rows)) != len(check_list_of_rows):
                    count += 1
            check_list_of_rows.clear()
            for i in range(0, 3):
                check_list_of_rows.clear()
                for j in list_of_rows_2:
                    obj_label = getattr(self, "lineEdit_{}".format(j + 3 * i))
                    if 1 <= int(obj_label.text()) <= 9:
                        check_list_of_rows.append(int(obj_label.text()))
                    else:
                        self.label.setText('Найден неверный символ!')
                if len(set(check_list_of_rows)) != len(check_list_of_rows):
                    count += 1
            check_list_of_rows.clear()
            for i in range(0, 3):
                check_list_of_rows.clear()
                for j in list_of_rows_3:
                    obj_label = getattr(self, "lineEdit_{}".format(j + 3 * i))
                    if 1 <= int(obj_label.text()) <= 9:
                        check_list_of_rows.append(int(obj_label.text()))
                    else:
                        self.label.setText('Найден неверный символ!')
                if len(set(check_list_of_rows)) != len(check_list_of_rows):
                    count += 1
            """В следующих 3 циклах идет проверка на правильное заполнение 
                            квадратов в судоку"""
            for i in list_of_squares:
                check_list_of_squares.clear()
                for j in range(i[0], i[1]):
                    obj_label = getattr(self, "lineEdit_{}".format(j))
                    if 1 <= int(obj_label.text()) <= 9:
                        check_list_of_squares.append(int(obj_label.text()))
                    else:
                        self.label.setText('Найден неверный символ!')
                if len(set(check_list_of_squares)) != len(check_list_of_squares):
                    count += 1
            if count == 0:
                self.label.setText('Всё верно!')
                self.add_points()
            else:
                self.label.setText('Найдены ошибки!')
        else:
            self.label.setText('Найден неверный символ!')

    """Метод для начисления очков к личному прогрессу.
    Происходит подключение к базе данных accounts и взятие из таблицы
    points значения очков пользователя по его id. При правильном решении
    судоку легкого уровня к уже имеющимся очкам пользователя начисляется
    25 очков, среднего - 50 очков, а сложного - 75 очков."""

    def add_points(self):  # метод для добавления очков пользователю при
        # правильном решении судоку
        self.conn = sqlite3.connect('accounts.db')
        self.cur = self.conn.cursor()
        self.point = self.cur.execute(f"""SELECT marks FROM points
                                        WHERE id = {self.id}""").fetchall()  # взятие
        # значения количества очков у пользователя
        if self.point_light_level == 1:  # добавление очков пользователю, правильно
            # решившему судоку на легком уровне
            self.label_2.setText('К личному прогрессу добавлено 25 очков.')
            self.new_point = self.point[0][0] + 25
            self.cur.execute(f"""UPDATE points
                        SET marks = {self.new_point}
                        WHERE id = {self.id}""")
            self.conn.commit()
            self.point_light_level = 0
        elif self.point_middle_level == 1:  # добавление очков пользователю, правильно
            # решившему судоку на среднем уровне
            self.label_2.setText('К личному прогрессу добавлено 50 очков.')
            self.new_point = self.point[0][0] + 50
            self.cur.execute(f"""UPDATE points
                        SET marks = {self.new_point}
                        WHERE id = {self.id}""")
            self.conn.commit()
            self.point_middle_level = 0
        elif self.point_high_level == 1:  # добавление очков пользователю, правильно
            # решившему судоку на сложном уровне
            self.label_2.setText('К личному прогрессу добавлено 75 очков.')
            self.new_point = self.point[0][0] + 75
            self.cur.execute(f"""UPDATE points
                        SET marks = {self.new_point}
                        WHERE id = {self.id}""")
            self.conn.commit()
            self.point_high_level = 0

    """Метод среднего уровня игры.
        В нем идет подключение к ui-файлу game.ui игры, QLineEdit'ы
        (то есть сами клетки игры) заполняются заданными в словаре значениями"""

    def middle_level(self):  # метод для игры в судоку на среднем уровне
        uic.loadUi('game.ui', self)  # подключение к ui-файлу игры
        self.setWindowIcon(QIcon("sudoku.png"))
        # добавление иконки в окно приложения
        self.point_middle_level = 1
        for i in range(1, 82):
            obj_label = getattr(self, "lineEdit_{}".format(i))
            # возвращает значение атрибута указанного объекта по его имени
            font = QFont()
            font.setPointSize(20)
            obj_label.setFont(font)
            obj_label.setAlignment(Qt.AlignCenter)
            # установка текста по центру
        self.dict = {1: '5', 2: '6', 3: '8', 10: '7', 11: '1', 12: '4', 13: '6',
                     16: '5', 23: '5', 24: '8', 28: '9', 32: '3', 33: '5',
                     34: '7', 36: '1', 40: '2', 42: '7', 44: '5', 46: '5',
                     49: '8', 53: '6', 58: '2', 60: '9', 61: '4', 62: '7',
                     65: '6', 66: '2', 67: '4', 68: '7', 73: '7', 79: '2',
                     80: '1'}  # словарь, где ключами являются номера виджетов
        # QLineEdit, а значения - числа, которые кладутся в клетки судоку
        for i in self.dict.keys():  # в данном цикле идет заполнение клеток
            # судоку числами из словаря
            obj_label = getattr(self, "lineEdit_{}".format(i))
            obj_label.setText(self.dict[i])
            obj_label.setEnabled(False)
            obj_label.setAlignment(Qt.AlignCenter)
        self.pushButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.use_hint)

    """Метод сложного уровня игры.
        В нем идет подключение к ui-файлу game.ui игры, QLineEdit'ы
        (то есть сами клетки игры) заполняются заданными в словаре значениями"""

    def high_level(self):  # метод для игры в судоку на сложном уровне
        uic.loadUi('game.ui', self)  # подключение к ui-файлу игры
        self.setWindowIcon(QIcon("sudoku.png"))
        # добавление иконки в окно приложения
        self.point_high_level = 1
        for i in range(1, 82):
            obj_label = getattr(self, "lineEdit_{}".format(i))
            # возвращает значение атрибута указанного объекта по его имени
            font = QFont()
            font.setPointSize(20)
            obj_label.setFont(font)
            obj_label.setAlignment(Qt.AlignCenter)
            # установка текста по центру
        self.dict = {1: '4', 12: '8', 13: '7', 17: '9', 18: '1', 21: '2',
                     26: '7', 29: '1', 31: '6', 35: '5', 37: '5', 39: '6',
                     42: '4', 50: '9', 52: '8', 55: '3', 56: '4', 58: '8',
                     62: '2', 66: '2', 68: '3', 70: '8', 71: '1', 75: '1',
                     78: '6'}  # словарь, где ключами являются номера виджетов
        # QLineEdit, а значения - числа, которые кладутся в клетки судоку
        for i in self.dict.keys():  # в данном цикле идет заполнение клеток
            # судоку числами из словаря
            obj_label = getattr(self, "lineEdit_{}".format(i))
            obj_label.setText(self.dict[i])
            obj_label.setEnabled(False)
            obj_label.setAlignment(Qt.AlignCenter)
        self.pushButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.use_hint)

    """Метод для возврата назад к главному окну.
    Происходит возврат пользователя к главному окну при нажатии кнопки
    "Назад" в окне игры."""

    def back(self):  # метод для возврата к главному окну программы
        self.point_light_level = 0
        self.point_middle_level = 0
        self.point_high_level = 0
        self.hide()
        self.second_form = Sudoku(self.id, self.name)
        self.second_form.show()

    """Метод открытия окна справки.
    Происходит подключение к классу Info при выполнении действий в меню"""

    def info(self):  # метод для открытия справки
        self.hide()
        self.second_form = Info(self.id, self.name)
        self.second_form.show()

    """Метод открытия окна с прогрессом.
    Происходит подключение к классу Progress при выполнении действий в меню"""

    def show_my_progress(self):  # метод для показа прогресса пользователя
        self.hide()
        self.second_form = Progress(self.id, self.name)
        self.second_form.show()

    """Метод для подсказки.
    Происходит помещение дополнительных чисел в клетки на поле
    игры, в зависимости от выбранного уровня игры, что упрощает 
    решение самой игры."""

    def use_hint(self):  # метод для использования подсказок
        if self.point_light_level == 1:  # использоваание подсказки,
            # если пользователь играет в судоку на легком уровне
            self.light_hint = [1, 24, 33, 67]
            for i in self.light_hint:
                obj_label = getattr(self, "lineEdit_{}".format(i))
                obj_label.setText('8')
                obj_label.setEnabled(False)
                obj_label.setAlignment(Qt.AlignCenter)
        elif self.point_middle_level == 1:  # использоваание подсказки,
            # если пользователь играет в судоку на среднем уровне
            self.middle_hint = [4, 25, 37, 51, 56, 69]
            for i in self.middle_hint:
                obj_label = getattr(self, "lineEdit_{}".format(i))
                obj_label.setText('1')
                obj_label.setEnabled(False)
                obj_label.setAlignment(Qt.AlignCenter)
        elif self.point_high_level == 1:  # использоваание подсказки,
            # если пользователь играет в судоку на сложном уровне
            self.high_hint = [14, 27, 36, 47, 67, 79]
            for i in self.high_hint:
                obj_label = getattr(self, "lineEdit_{}".format(i))
                obj_label.setText('4')
                obj_label.setEnabled(False)
                obj_label.setAlignment(Qt.AlignCenter)


"""Класс для открытия окна со справкой"""


class Info(QMainWindow):
    """При инициализации отображает окно со справкой к программе,
     получает в аргументах id пользователя и его имя."""
    def __init__(self, id, name):
        super(Info, self).__init__()
        uic.loadUi('info.ui', self)
        self.setWindowIcon(QIcon("sudoku.png"))
        self.id = id
        self.name = name
        self.pushButton.clicked.connect(self.back)

    """Метод возврата к главному окну.
    Происходит возврат пользователя к главному классу Sudoku."""

    def back(self):
        self.hide()
        self.second_form = Sudoku(self.id, self.name)
        self.second_form.show()


"""Класс для открытия окна с личным прогрессом пользователя"""


class Progress(QMainWindow):
    """При инициализации отображает окно с информацией о личном
    прогрессе пользователя, получает в аргументах id пользователя
    и его имя, в label помещается текст с приветствием пользователя
    по имени и строка с количеством очков у пользователя в текущий
    момент времени."""
    def __init__(self, id, name):
        super(Progress, self).__init__()
        self.conn = sqlite3.connect('accounts.db')
        self.cur = self.conn.cursor()
        self.id = id
        self.name = name
        uic.loadUi('progress.ui', self)
        self.setWindowIcon(QIcon("sudoku.png"))
        self.points = self.cur.execute("""SELECT marks FROM points
                                WHERE id = ?""", (self.id,)).fetchall()  # получение
        # значения количества очков, заработанных пользователем
        self.label.setText('Здравствуйте, ' + self.name + '!')  # приветствие пользователя
        self.label_2.setText('На вашем счёте на данный момент ' + str(self.points[0][0]) +
                             ' очков.')  # информация о количестве очков пользователя
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.pushButton.clicked.connect(self.back)

    """Метод возврата к главному окну.
        Происходит возврат пользователя к главному классу Sudoku."""

    def back(self):  # метод для возврата к главному окну программы
        self.hide()
        self.second_form = Sudoku(self.id, self.name)
        self.second_form.show()


"""Класс для вывода диалоговых окон для входа и регистрации"""


class Dialog(QDialog):
    """При инициализации подключает базу данных accounts и отображает
     окно с двумя кнопками "Да" и "Нет". При положительном ответе идет
      вызов метода check_info и подключение к ui-файлу dialog_2.ui с
      окном для входа, при отрицательном ответе вызывается метод
      insert_in_table и вызывается ui-файл dialog.ui с формой для
      регистрации."""
    def __init__(self):
        super(Dialog, self).__init__()
        msg = QMessageBox(self)  # создание диалогового окна для получения
        # данных о том, что был ли зарегистрирован пользователь до этого или нет
        self.conn = sqlite3.connect('accounts.db')  # подключение к базе данных
        # с информацией о пользователях
        self.cur = self.conn.cursor()
        msg.setWindowTitle("Судоку")
        self.setWindowIcon(QIcon("sudoku.png"))
        msg.setIcon(QMessageBox.Question)
        msg.setText('Вы пользовались ранее данным приложением "Судоку"?')
        self.conn.commit()
        yes_button = msg.addButton("Да", QMessageBox.YesRole)
        no_button = msg.addButton("Нет", QMessageBox.RejectRole)
        msg.setDefaultButton(yes_button)
        msg.exec_()
        if msg.clickedButton() == yes_button:  # вывод формы для входа при
            # положительном ответе пользователя
            uic.loadUi('dialog_2.ui', self)
            self.setWindowIcon(QIcon("sudoku.png"))
            self.pushButton.clicked.connect(self.check_info)
            self.pushButton_2.clicked.connect(self.back)
        elif msg.clickedButton() == no_button:  # вывод формы для регистрации
            # при отрицательном ответе пользователя
            uic.loadUi('dialog.ui', self)
            self.setWindowIcon(QIcon("sudoku.png"))
            self.btn.clicked.connect(self.insert_in_table)
            self.btn_1.clicked.connect(self.back)

    """Метод возврата к прошлому окну"""
    def back(self):
        self.hide()
        self.second_form = Dialog()
        self.second_form.show()

    """Метод проверки введенных данных при входе.
     Происходит проверка по базе данных введенных пользователем строк
     в QLineEdit. При успешной проверке происходит переход к классу 
     Sudoku(то есть к главному окну)"""

    def check_info(self):  # проверка наличия аккаунта пользователя в базе данных
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.id = self.cur.execute("""SELECT id FROM users
                                WHERE username = ? and password = ?""", (username, password)).fetchall()
        # получение id пользователя
        self.name = self.cur.execute("""SELECT name FROM users
                        WHERE username = ? and password = ?""", (username, password)).fetchall()
        # получение имени пользователя
        if len(self.id) == 1:  # если найден только 1 человек в данным никнеймом и паролем,
            # то выполняется следующая часть программы
            self.conn.commit()
            self.hide()
            self.second_form = Sudoku(self.id[0][0], self.name[0][0])  # переход к главному окну
            self.second_form.show()
        else:
            self.label_3.setText('Неверное имя пользователя или пароль')
            self.conn.commit()

    """Метод регистрации пользователя.
    В нем происходит внесение введенных пользователем данных в окне для
    регистрации в таблицу users базы данных accounts, внесение в таблицу
    users уникального id, генерируемого программой случайно с помощью 
    библиотеки random, внесение в таблицу points данных о пользователе(id,
    имя и количество очков(начальное значение очков равно 0) и происходит
    переход к классу Sudoku(то есть к главному окну)."""

    def insert_in_table(self):
        username = self.lineEdit.text()  # получение никнейма из QLineEdit
        password = self.lineEdit_3.text()  # получение пароля из QLineEdit
        name = self.lineEdit_2.text()  # получение имени из QLineEdit
        if username == '' or password == '' or name == '':
            self.label_4.setText('Заполните все необходимые поля!')
        else:
            random_num = random.randint(1, 10000000000)  # создание
            # уникального id для пользователя
            self.vals = (random_num, username, password, name)
            self.vals_2 = (random_num, name, 0)
            self.cur.execute(f'INSERT INTO users(id,username,password,name) '
                             f'VALUES {self.vals}')
            # внесение данных о пользователе в таблицу users в базу данных accounts
            self.conn.commit()
            self.cur.execute(f'INSERT INTO points(id,name,marks) VALUES {self.vals_2}')
            # внесение данных о пользователе в таблицу points в базу данных accounts
            self.conn.commit()
            self.hide()
            self.second_form = Sudoku(self.vals[0], self.vals[3])  # открытие
            # главного окна
            self.second_form.show()


"""Метод исключений.
При возникающей ошибке в консоль выводится тип ошибки и где именно она возникла"""


def except_hook(cls, exeption, traceback):
    sys.__excepthook__(cls, exeption, traceback)


"""Конструкция отвечающая за запуск игры"""
if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec())
