from datetime import date

from src.schemas.bookings import BookingAdd, Booking
from src import models


async def test_booking_crud(db):
    # test create
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_add = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2023, month=12, day=12),
        date_to=date(year=2024, month=1, day=1),
        price=100,
    )
    booking: Booking = await db.bookings.add(booking_add)
    await db.commit()
    print(f"{booking=}")

    assert booking
    assert booking.user_id == user_id
    assert booking.room_id == room_id
    assert booking.date_from == booking_add.date_from

    # test read
    new_booking: Booking = await db.bookings.get_one_or_none(id=booking.id)
    assert new_booking
    assert new_booking == booking
    print("read ok")
    # test update

    id = booking.id

    old_booking = booking.model_copy()

    booking.price = 200
    booking.date_to = date(year=2024, month=2, day=1)
    booking.date_from = date(year=2025, month=1, day=23)

    booking_add = BookingAdd(**booking.model_dump())

    await db.bookings.edit(booking_add, id=id)
    new_booking = await db.bookings.get_one_or_none(id=id)
    assert new_booking != old_booking
    assert new_booking == booking
    print("update ok")

    # test delete

    await db.bookings.delete(id=id)
    assert not await db.bookings.get_one_or_none(id=id)

    print("delete ok")
