"""Консольный вариант игры Sea Battle"""

from abc import ABC, abstractmethod
from random import randint
import time

DESCRIPTION = """
Игра морской бой
Человек vs ИИ
Поле: 6 х 6
Корабли: 3х палубник - 1, 2х палубник -2, 1х палубник -4
ПОЕХАЛИ:
"""


class MySeaBattleException(Exception):  # общее исключение для классов игры
    pass


class MissException(MySeaBattleException):
    def __str__(self):
        print("Удар мимо доски")


class RepeatException(MySeaBattleException):
    def __str__(self):
        print("Повторный выстрел в точку")


class BusyException(MySeaBattleException):
    def __str__(self):
        print("Эта клетка уже занята")


class BoardWrongShipException(MySeaBattleException):
    pass


class Dot:
    """
    Класс представления координаты в поле игры.
    Атрибуты:
    x : int
        положение по горизонтали
    y : int
        положение по вертикали
    Методы:
    __init__ - инизиализатор/конструктор объекта
    __eq__ - функция сравнения объектов между собой
    __str__ - функция строкового представления объекта
    info -
    """
    point = None

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.point = (x-1, y-1)  # значение точки расположения, 2 координаты(Х,Y), кортеж, -1 т.к я использую индексы, а они стартуют с 0, 1 поле с 1

    @property
    def get_point(self):
        return self.point   # функция геттер, для возврата значения в алгоритм вне класса кортежа с позицией точки, в этой версии программы не использую

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"{self.x},{self.y}"

    @staticmethod
    def GET_INFO():
        print("Это класс для объявления координат")


class Ship:
    """
    Класс представления корабля в игре
    """

    def __init__(self, longer, first_point, direction):
        self.longer = longer            # длинна корбля, допустимые значения: 1,2,3
        self.first_point = first_point  # значения возвращиемый из класса Dot
        self.direction = direction      # если True, то располагаем корабль по горизонтали
        self.count_life = longer        # жизни корбля = длинна корабля, допустимые значения: 1 или 2 или 3

    @property  # декоратор для доступа к функции dots(), не как к функции, а как свойству(без () )
    def dots(self):
        """ функция установки положения корабля по его начальной координате,
         с учетом длинны и направлении гор/верт """
        ship = []
        for point in range(self.longer):  # цикл проходит все точки корабля в зависимости от заданной длинны корабля
            x = self.first_point.x  # вычисляем координату первой точки по оси Х
            y = self.first_point.y  # вычисляем координату первой точки по оси Y
            if self.direction:       # расположение корабля по горизонтали
                x += point           # добавлеям следующую точку по оси Х в цикле
            else:                    # расположение корабля по вертикали
                y += point
            ship.append(Dot(x, y))
        return ship

    def shooten(self, shot):
        return shot in self.dots


class Board:
    """
    Класс хранит данные о доске,ее размеры, корабли
    """

    def __init__(self, hid, size: int) -> None:
        self.hid = hid
        self.size = size
        self.play_field = [["0" for x in range(size)] for y in range(size)]
        self.count = 0
        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "x\y| 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.play_field, start=1):
            res += f"\n{i}  |  " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def add_ship(self, ship):
        """Функция добавления корабля на игровое поле"""

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.play_field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        """Функция-аниматор, ставит точку в позицию между кораблями, т.к должно быть расстояние между кораблями(минимум 1 точка)"""
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.play_field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def out(self, dot):
        """Функция-указатель, попала ли точка в игровое поле"""
        if (0 <= dot.x < 6) and (0 <= dot.y < 6):
            return False
        else:
            return True

    def shot(self, point):
        """Функция-выстрел, если мимо цели или повторно в ту же точку, то исключение,
        если убили/ранили корабль, то ставим "X" и сообщаем о попадании"""
        if self.out(point):
            raise MissException

        elif point in self.busy:
            raise RepeatException

        self.busy.append(point)

        for ship in self.ships:
            if point in ship.dots:
                ship.count_life -= 1
                self.play_field[point.x][point.y] = "X"
                if ship.count_life == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.play_field[point.x][point.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player(ABC):
    """
    Абстрактый класс игрока, содержит абстрактный метод ask(),
    нельзя создвть его экземпляр, необходимо наследовать и в
    потомке переопределять метод ask
    """
    def __init__(self, my_board: Board, war_board: Board) -> None:
        self.my_board = my_board
        self.war_board = war_board

    #  абстрактный метод вопроса, его обязательно переопределить в классах потомках
    @abstractmethod
    def ask(self):
        print("Обдумывание над ходом... дайте секунду")
        time.sleep(1)

    #  общий метод, его унаследуют все потомки
    def move(self):
        while True:
            try:
                hit = self.ask()
                repeat = self.war_board.shot(hit)
                return repeat
            except MySeaBattleException as ex:
                print(ex)


class AI(Player):
    def ask(self):
        super().ask()
        hit = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {hit.x +1} {hit.y +1}")
        return hit


class User(Player):
    def ask(self):
        super().ask()
        while True:
            try:
                x = int(input("Ваш ход  по оси X: "))
                y = int(input("Ваш ход по оси Y:"))
            except ValueError:
                print("Вы ввели не число")
                continue

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(hid=False, size=6)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print(DESCRIPTION)

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.my_board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.my_board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.my_board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.my_board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


def main():
    play = Game()
    play.start()


if __name__ == "__main__":
    main()