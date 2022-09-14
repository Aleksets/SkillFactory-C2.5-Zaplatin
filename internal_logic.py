from exceptions import UnableToDeployShipError


# класс "Точка" с координатами x и y
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # определение особенностей проверки эквивалентности точки другим точкам
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# класс "Корабль" с параметрами длина, стартовая точка и вертикальное/горизонтальное расположение
class Ship:
    def __init__(self, length, start, position_vertical):
        self.length = length
        self.start = start
        self.position_vertical = position_vertical
        # параметр жизни, в момент инициализации равен длине корабля
        self.lives = length

    # метод возвращает список точек, занимаемых кораблём на доске
    def dots(self):
        dots = []
        for part in range(self.length):
            if self.position_vertical:
                dots.append(Dot(self.start.x, self.start.y + part))
            else:
                dots.append(Dot(self.start.x + part, self.start.y))
        return dots


# класс 'Доска' с параметрами состояние точек на доске, корабли на доске,
# скрыты ли корабли при отрисовке, количество активных кораблей на доске
class Board:
    def __init__(self, hid):
        self.dots_conditions = list(map(list, [[" "] * 6] * 6))
        self.ships = []
        self.hid = hid
        self.live_ships = 0

    # метод возвращает True, если точка на доске
    @staticmethod
    def out(dot, j=0, k=0):
        if (0 <= dot.x + j <= 5) and (0 <= dot.y + k <= 5):
            return False
        else:
            return True

    # метод добавляет корабль на доску
    def add_ship(self, new_ship):
        for dot in new_ship.dots():
            if self.dots_conditions[dot.x][dot.y] != " ":
                raise UnableToDeployShipError
        for dot in new_ship.dots():
            self.dots_conditions[dot.x][dot.y] = "■"
        self.ships.append(new_ship)
        self.live_ships += 1
        self.contour(new_ship, "O")

    # метод "обводит" корабль по контуру, чтобы в соседних ячейках нельзя было разместить другие корабли
    def contour(self, ship, marker):
        for i in ship.dots():
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if not self.out(i, j, k):
                        if marker == "O":
                            if self.dots_conditions[i.x + j][i.y + k] == " ":
                                self.dots_conditions[i.x + j][i.y + k] = marker
                        else:
                            if self.dots_conditions[i.x + j][i.y + k] == "O":
                                self.dots_conditions[i.x + j][i.y + k] = marker

    # метод отрисовки доски в командной строке в зависимости от параметра hid
    def draw(self):
        print("Доска противника") if self.hid else print("Ваша доска")
        print(" |1|2|3|4|5|6|")
        for i, j in enumerate(self.dots_conditions):
            print(f"{i + 1}|", end="")
            for k in j:
                if not self.hid:
                    if k == "O":
                        print(f" |", end="")
                    else:
                        print(f"{k}|", end="")
                else:
                    if k == "■" or k == "O":
                        print(f" |", end="")
                    else:
                        print(f"{k}|", end="")
            print("\r")

    # метод производит выстрел по заданной точке с оценкой степени поражения кораблей на доске
    def shot(self, dot):
        for i in range(len(self.ships)):
            if dot in self.ships[i].dots():
                self.dots_conditions[dot.x][dot.y] = "X"
                self.ships[i].lives -= 1
                if not self.ships[i].lives:
                    self.live_ships -= 1
                    print('Корабль уничтожен!!!')
                    self.contour(self.ships[i], "О")
                else:
                    print("Корабль повреждён!")
                self.draw()
                input("Нажмите Enter")
                return True if self.live_ships else False
        else:
            print("Промах")
            self.dots_conditions[dot.x][dot.y] = "T"
            self.draw()
            input("Нажмите Enter")
            return False
