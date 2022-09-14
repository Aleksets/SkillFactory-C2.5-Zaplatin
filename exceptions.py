# Родительский класс исключений
class CustomException(Exception):
    def __init__(self):
        self.message = ""

    def __str__(self):
        return f"{self.message}"


# Дочерний класс исключения ошибки ввода точки в неверном формате
class DotFormatError(CustomException):
    def __init__(self):
        self.message = "Вы нарушили формат ввода. Попробуйте снова"


# Дочерний класс исключения ошибки стрельбы в уже отмеченную точку
class ShotMakesNoSenseError(CustomException):
    def __init__(self):
        self.message = "Нет смысла стрелять в эту точку. Попробуйте снова"


# Дочерний класс исключения ошибки ввода точки вне доски
class BoardOutError(CustomException):
    def __init__(self):
        self.message = "Координаты могут быть только целыми числами в интервале [1;6]. Попробуйте снова"


# Дочерний класс исключения ошибки размещения корабля на доске
class UnableToDeployShipError(CustomException):
    def __init__(self):
        self.message = "Невозможно разместить корабль с заданными начальными параметрами"


# Дочерний класс исключения ошибки оценки желания продолжать игру
class WannaPlayCheckError(CustomException):
    def __init__(self):
        self.message = "Необходимо ввести 'y' или 'n'. Попробуйте снова"
