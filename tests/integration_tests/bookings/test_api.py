import pytest

from src.schemas.bookings import Booking
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@pytest.fixture(scope="session")
async def delete_all_bookings():
    async with DBManager(async_session_maker_null_pool) as db:
        bookings: list[Booking] = await db.bookings.get_all()
        for b in bookings:
            await db.bookings.delete(id=b.id)
        await db.commit()

        new_bookings = await db.bookings.get_all()
        print(f"Удаление bookings {new_bookings=}")
        assert not new_bookings


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-01-01", "2024-02-02", 200),
        (1, "2024-01-01", "2024-02-02", 200),
        (1, "2024-01-01", "2024-02-02", 200),
        (1, "2024-01-01", "2024-02-02", 200),
        (1, "2024-01-01", "2024-02-02", 200),
        (1, "2024-01-01", "2024-02-02", 400),
        (1, "2024-03-01", "2024-04-02", 200),
        (1, "2024-03-01", "2024-04-02", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac):

    request_json = {"date_from": date_from, "date_to": date_to, "room_id": room_id}

    response = await authenticated_ac.post(
        "/bookings",
        json=request_json,
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "room_id, date_from, date_to, quantity",
    [
        (1, "2024-01-01", "2024-02-02", 1),
        (1, "2024-01-01", "2024-02-02", 2),
        (1, "2024-01-01", "2024-02-02", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, quantity, authenticated_ac, delete_all_bookings
):
    request_json = {"date_from": date_from, "date_to": date_to, "room_id": room_id}

    response = await authenticated_ac.post(
        "/bookings",
        json=request_json,
    )

    assert response.status_code == 200

    me_response = await authenticated_ac.get("/bookings/me")
    data = me_response.json()
    assert len(data) == quantity
