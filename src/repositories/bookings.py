from sqlalchemy import select
from datetime import date

from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking, BookingAdd
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model: BookingsOrm = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    # async def add(self, data: BookingAdd) -> Booking:
    #     insert_stmt = (
    #         insert(self.model).values(**data.model_dump()).returning(self.model)
    #     )
    #     result = await self.session.execute(insert_stmt)
    #     model = result.scalars().one()
    #     return self.mapper.map_to_domain_entity(model)
