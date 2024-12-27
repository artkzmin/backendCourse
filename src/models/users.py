from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.database import BaseOrm


class UsersOrm(BaseOrm):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
