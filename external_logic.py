import random

from exceptions import DotFormatError
from exceptions import ShotMakesNoSenseError
from exceptions import BoardOutError
from exceptions import UnableToDeployShipError
from exceptions import WannaPlayCheckError

from internal_logic import Board
from internal_logic import Ship
from internal_logic import Dot


# родительский класс 'Игрок' с параметрами своя доска, доска противника
class Player:
    def __init__(self, my_board, foe_board):
        self.my_board = my_board
        self.foe_board = foe_board
        # параметр выигрыша игрока
        self.win = False

    # метод запроса координат точки стрельбы, переопределяется в дочерних классах
    def ask(self):
        pass

    # метод совершения хода, возвращает True, если в процессе хода было попадание по кораблю
    def move(self):
        if self.foe_board.shot(self.ask()):
            return True
        else:
            return False


# дочерний класс игрока-ИИ
class AI(Player):
    # переопределение родительского метода. Возвращает точку, координаты которой получены случайным образом
    # на доске с проверкой бессмысленности стрельбы в указанную точку
    def ask(self):
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            if self.foe_board.dots_conditions[x][y] != "X" and \
                    self.foe_board.dots_conditions[x][y] != "T" and \
                    self.foe_board.dots_conditions[x][y] != "О":
                break
        print(f"Ход противника. Координаты стрельбы '{x + 1} {y + 1}'")
        return Dot(x, y)


# дочерний класс игрока-человека
class User(Player):
    # переопределение родительского метода. Возвращает точку, координаты которой вводятся с клавиатуры
    # с проверкой правильности формата ввода и бессмысленности стрельбы в указанную точку
    def ask(self):
        while True:
            try:
                step = input(f"Ваш ход. Введите координаты стрельбы в формате '№строки №столбца': ")
                step = " ".join(step.split())
                if len(step) == 3 and len(step.replace(" ", "")) == 2 and \
                        step.replace(" ", "").isdigit():
                    step = tuple(map(int, step.split(" ")))
                    step = Dot(step[0] - 1, step[1] - 1)
                    if not self.foe_board.out(step):
                        if self.foe_board.dots_conditions[step.x][step.y] != "X" and \
                                self.foe_board.dots_conditions[step.x][step.y] != "T" and \
                                self.foe_board.dots_conditions[step.x][step.y] != "О":
                            break
                        else:
                            raise ShotMakesNoSenseError
                    else:
                        raise BoardOutError
                else:
                    raise DotFormatError
            except ShotMakesNoSenseError as e:
                print(e.message)
            except BoardOutError as e:
                print(e.message)
            except DotFormatError as e:
                print(e.message)
        return step


# класс 'Игра' - основной класс с параметрами доски игрока-человека, доски игрока-ИИ,
# игрока-человека, игрока-ИИ, очередности первого хода
class Game:
    def __init__(self):
        self.user_board = self.random_board(False)
        self.ai_board = self.random_board(True)
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)
        self.user_move = random.randint(0, 1)

    # метод размещает корабли на доске с проверкой возможности этого размещения
    @staticmethod
    def random_board(hid):
        ships2deploy = (3, 2, 2, 1, 1, 1, 1)
        while True:
            board = Board(hid)
            deployed_ships = 0
            while deployed_ships < len(ships2deploy):
                s_len = ships2deploy[deployed_ships]
                count = 0
                while count < 1000:
                    try:
                        vert = random.randint(0, 1)
                        if vert:
                            start = Dot(random.randint(0, 5), random.randint(0, 5 - s_len + 1))
                        else:
                            start = Dot(random.randint(0, 5 - s_len + 1), random.randint(0, 5))
                        board.add_ship(Ship(s_len, start, vert))
                        deployed_ships += 1
                        break
                    except UnableToDeployShipError:
                        count += 1
                else:
                    break
            else:
                break
        return board

    # метод 'приветствие', описывает особенности игры и определяет желание играть (с проверкой ввода)
    def greet(self):
        if not self.ai.win and not self.user.win:
            random.seed()
            print("""
Добро пожаловать в игру 'Морской бой'!
Автор: Заплатин Алексей

Правила игры отличаются от канонических:
- поле 6x6;
- кораблей у каждого игрока всего 7:
    - 1 трёхпалубный;
    - 2 двухпалубных;
    - 4 однопалубных;
- корабли расставляются автоматически.
Дополнительные особенности:
- против вас играет ИИ;
- право первого хода определяется случайным образом.
Следование инструкциям гарантирует получение наслаждения от игры.""")
        else:
            self.__init__()
        while True:
            try:
                answer = input("Желаете начать новую игру (y/n)? ").lower()
                if answer == "y" or answer == "n":
                    break
                else:
                    raise WannaPlayCheckError
            except WannaPlayCheckError as e:
                print(e.message)
        if answer == "y":
            print("Успехов!")
            return True
        else:
            print("Будем рады видеть вас снова!")
            return False

    # метод основного цикла игры, выполняет поочередно шаги обоих игроков до победы одного из них
    def loop(self):
        self.user.my_board.draw()
        self.user.foe_board.draw()
        if self.user_move:
            while self.user.move():
                pass
            if not self.user.foe_board.live_ships:
                print("Вы победили! Поздравляем!")
                self.user.win = True
        else:
            while self.ai.move():
                pass
            if not self.ai.foe_board.live_ships:
                print("Сегодня не повезло, но мы за вас болели")
                self.ai.win = True
        self.user_move = False if self.user_move else True
        print("---------------------------------------------------------------")

    # метод 'старт' инициирует игру, запускает в цикле методы greet и loop
    def start(self):
        while self.greet():
            while not self.ai.win and not self.user.win:
                self.loop()


# инициализация и запуск игры
game = Game()
game.start()
