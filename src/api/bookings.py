from fastapi import APIRouter, Body, HTTPException, status

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest, Booking
from src.exceptions import ObjectNotFountException
from src.schemas.hotels import Hotel
from src.exceptions import AllRoomsAreBooked

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep) -> list[Booking]:
    return await db.bookings.get_all()


@router.get("/me")
async def get_me_bookings(db: DBDep, user_id: UserIdDep) -> list[Booking]:
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFountException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Номер не найден')

    _booking_data = BookingAdd(
        user_id=user_id, price=room.price, **booking_data.model_dump()
    )
    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    try:
        booking_data = await db.bookings.add_booking(
            data=_booking_data, hotel_id=hotel.id
        )
        await db.commit()
        return {"status": "OK", "data": booking_data}
    except AllRoomsAreBooked as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.detail)
