from fastapi import APIRouter, Body, HTTPException, status

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest, Booking

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep) -> list[Booking]:
    return await db.bookings.get_all()


@router.get("/me")
async def get_me_bookings(db: DBDep, user_id: UserIdDep) -> list[Booking]:
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(
    user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()
):
    price = (await db.rooms.get_one_or_none(id=booking_data.room_id)).price

    _booking_data = BookingAdd(
        user_id=user_id, price=price, **booking_data.model_dump()
    )
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    try:
        booking_data = await db.bookings.add_booking(
            data=_booking_data, hotel_id=hotel.id
        )
        await db.commit()
        return {"status": "OK", "data": booking_data}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
