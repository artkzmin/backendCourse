from fastapi import APIRouter, Body

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAddRequest, Booking
from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    AllRoomsAreBookedHTTPException,
    AllRoomsAreBooked,
)
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep) -> list[Booking]:
    return await BookingService(db).get_all()


@router.get("/me")
async def get_me_bookings(db: DBDep, user_id: UserIdDep) -> list[Booking]:
    return await BookingService(db).get_filtered(user_id)


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()):
    try:
        booking_data = await BookingService(db).add_booking(
            user_id=user_id, booking_data=booking_data
        )
    except AllRoomsAreBooked:
        raise AllRoomsAreBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK", "data": booking_data}
