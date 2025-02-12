from datetime import date

from src.schemas.bookings import BookingAdd, Booking
from src import models


async def test_booking_crud(db):
    # test create
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2023, month=12, day=12),
        date_to=date(year=2024, month=1, day=1),
        price=100,
    )
    new_booking_data: Booking = await db.bookings.add(booking_data)
    await db.commit()
    print(f"{new_booking_data=}")

    # test read
    new_booking: Booking = await db.bookings.get_one_or_none(id=new_booking_data.id)
    assert new_booking == new_booking_data
    print("read ok")
    # test update

    id = new_booking_data.id

    old_booking = new_booking_data.model_copy()

    new_booking_data.price = 200
    new_booking_data.date_to = date(year=2024, month=2, day=1)
    new_booking_data.date_from = date(year=2025, month=1, day=23)

    booking_add = BookingAdd(**new_booking_data.model_dump())

    await db.bookings.edit(booking_add, id=id)
    new_booking = await db.bookings.get_one_or_none(id=id)
    assert new_booking != old_booking
    assert new_booking == new_booking_data
    print("update ok")

    # test delete

    await db.bookings.delete(id=id)
    assert await db.bookings.get_one_or_none(id=id) == None

    print("delete ok")
