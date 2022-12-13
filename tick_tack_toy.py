"""
Игра в кркстики-нолики
размер поля: 3х3
количество игроковЖ 2
"""

play_field = [['-', '-', '-'],
              ['-', '-', '-'],
              ['-', '-', '-']
              ]  # создание пустого поля

win_pos = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
           ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
           ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))  # кортеж, содержащий все выйгрышные позиции, аргумент для функции winner


def visual_field(func):
    """Декоратор для добавления верхней рамки для игрового поля"""
    def wrapper():
        print("Текущее состояние игрового поля")
        print("X/Y:  0    1    2")
        func()
    return wrapper


@visual_field
def field():
    """ Визуальное отображение поля, цикл проходит по вложенному списку,
     выводит его в виде матрицы 3х3, обернуто декоратором"""
    for el in range(len(play_field)):
        print(el, ":", play_field[el])


def winner(winner_pos):
    """ Функция определения победителя в игре"""
    for win in winner_pos:
        symbols = []
        for el in win:
            symbols.append(play_field[el[0]][el[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл игрок Х, Поздравляю")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл игрок 0, Поздравляю")
            return True
    return False


def play_game(elem):
    """ Тело игры, запрос ввода данных, проверка данных,
    счетчик номера хода, идентификация игрока ("Х"/"0"),
    определение победителя"""
    step_count = 0
    while True:
        x_pos = int(input("Введдите координату по Х: "))
        y_pos = int(input("Введдите координату по Y: "))
        if 0 > x_pos or x_pos > 2 or 0 > y_pos or y_pos > 2:
            print(" Координаты вне диапазона! ")
            continue
        if play_field[x_pos][y_pos] != "-":
            print(" Клетка занята! ")
            continue
        step = x_pos, y_pos
        if step_count % 2 != 1:
            elem[x_pos][y_pos] = "X"
            step_count += 1
            print("Ходит игрок X: ")
        else:
            elem[x_pos][y_pos] = "0"
            step_count += 1
            print("Ходит игрок 0: ")

        print(step)
        print("Ход № ", step_count)
        field()
        if winner(win_pos):
            break

        if step_count == 9:
            print(" Ничья!")
            break


def start_game():
    """ Функция - инициализация начала игры"""
    while True:
        answer = input("Начнем игру?(Y/N): ")
        if answer.lower() == "y":
            print("Отлично, поехали!")
            print("-----------------------")
            print("Начинает игру игрок Х: ")
            play_game(play_field)
        elif answer.lower() == "n":
            print("Игра окончена так и не начавшись!")
            break
        else:
            print("Я не понял ваш ответ, повторите")


if __name__ == "__main__":  # Исполняемая часть кода, работает локально из текщего модуля, не исполняется при импорте в другие модули
    field()
    start_game()
