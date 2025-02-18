from fastapi import HTTPException, status
from datetime import date


class BaseException(Exception):
    detail = "Ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class UserNotRegisteredException(BaseException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(BaseException):
    detail = "Пароль неверный"


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class AllRoomsAreBooked(BaseException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(BaseException):
    detail = "Похожий объект уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Дата заезда не может быть позже даты выезда",
        )


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Номер не найден"


class UserNotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"


class AllRoomsAreBookedHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Все номера заняты"


class UserAlreadyExistsHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с такой почтой уже существует"


class UserNotRegisteredHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не предоставлен токен"


class IncorrectTokenHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Некорректный токен"
