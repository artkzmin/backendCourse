from src.services.base import BaseService
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_all(self) -> list[Booking]:
        return await self.db.bookings.get_all()

    async def get_filtered(self, user_id) -> list[Booking]:
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, user_id, booking_data: BookingAddRequest) -> Booking:
        room = await RoomService(self.db).get_room_with_check(booking_data.room_id)

        _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        booking_data = await self.db.bookings.add_booking(data=_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking_data
