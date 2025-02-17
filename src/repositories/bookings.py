from sqlalchemy import select
from datetime import date

from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingAdd
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.exceptions import AllRoomsAreBooked


class BookingsRepository(BaseRepository):
    model: BookingsOrm = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        # query_hotel_id = select(RoomsOrm.hotel_id).filter_by(id=data.room_id)
        # res_hotel_id = await self.session.execute(query_hotel_id)
        # hotel_id = res_hotel_id.scalars().one()
        query = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )
        res = await self.session.execute(query)
        rooms_ids = res.scalars().all()
        if data.room_id in rooms_ids:
            return await self.add(data)
        raise AllRoomsAreBooked

    # async def add(self, data: BookingAdd) -> Booking:
    #     insert_stmt = (
    #         insert(self.model).values(**data.model_dump()).returning(self.model)
    #     )
    #     result = await self.session.execute(insert_stmt)
    #     model = result.scalars().one()
    #     return self.mapper.map_to_domain_entity(model)
