class BaseException(Exception):
    detail = 'Ошибка'
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFountException(BaseException):
    detail = 'Объект не найден'

class AllRoomsAreBooked(BaseException):
    detail = 'Не осталось свободных номеров'

class UserAlreadyExists(BaseException):
    detail = 'Пользователь уже существует'