from fastapi import APIRouter, HTTPException, status, Response

from passlib.context import CryptContext
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.base import StatusOK
from src.exceptions import ObjectAlreadyExists


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd) -> StatusOK:
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add_user(new_user_data)
        await db.commit()
    except ObjectAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь с такой почтой уже существует')
    return StatusOK


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким email не зарегистрирован",
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пароль неверный")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(user_id: UserIdDep, response: Response) -> StatusOK:
    response.delete_cookie("access_token")
    return StatusOK
