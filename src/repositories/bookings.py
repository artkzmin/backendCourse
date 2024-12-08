from sqlalchemy import insert

from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking, BookingAdd
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def add(self, data: BookingAdd) -> Booking:
        insert_stmt = (
            insert(self.model)
            .values(
                **data.model_dump()
            )
            .returning(self.model)
        )
        result = await self.session.execute(insert_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)
