from fastapi import APIRouter, Response

from passlib.context import CryptContext
from src.schemas.users import UserRequestAdd, User
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.base import StatusOK
from src.exceptions import (
    UserAlreadyExists,
    UserAlreadyExistsHTTPException,
    UserNotRegistered,
    UserNotRegisteredHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    IncorrectPassword,
    IncorrectPasswordHTTPException,
)


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd) -> StatusOK:
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExists:
        raise UserAlreadyExistsHTTPException
    return StatusOK


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotRegistered:
        raise UserNotRegisteredHTTPException
    except IncorrectPassword:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep) -> User:
    try:
        return await AuthService(db).get_user(user_id=user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post("/logout")
async def logout(user_id: UserIdDep, response: Response) -> StatusOK:
    response.delete_cookie("access_token")
    return StatusOK
