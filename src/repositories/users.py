from sqlalchemy import select
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
import logging

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import UserWithHashedPassword, UserAdd, User
from src.repositories.mappers.mappers import UserDataMapper
from src.exceptions import ObjectAlreadyExistsException


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model)

    async def add_user(self, data: UserAdd) -> User:
        try:
            return await self.add(data)
        except IntegrityError as ex:
            logging.exception(f"Не удалось добавить данные в БД, входные данные={data}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            logging.exception(f"Незнакомая ошибка, входные данные={data}")
            raise ex
