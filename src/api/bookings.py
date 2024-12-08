from fastapi import APIRouter, Body

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.post('')
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body()
):
    price = (await db.rooms.get_one_or_none(id=booking_data.room_id)).price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=price,
        **booking_data.model_dump()
    )
    booking_data = await db.bookings.add(data=_booking_data)
    await db.commit()
    return {
        'status': 'OK',
        'data': booking_data
    }
