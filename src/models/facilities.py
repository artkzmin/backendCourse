from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import BaseOrm


class FacilitiesOrm(BaseOrm):
    __tablename__ = 'facilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


class RoomsFacilitiesOrm(BaseOrm):
    __tablename__ = 'rooms_facilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'))
