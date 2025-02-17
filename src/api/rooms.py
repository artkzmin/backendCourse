from fastapi import APIRouter, Query, Body, HTTPException, status
from datetime import date
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, RoomAdd, RoomPatch
from src.schemas.base import StatusOK
from src.schemas.facilities import RoomFacilityAdd
from src.exceptions import ObjectNotFountException

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    pagination: PaginationDep,
    date_from: date = Query(examples=["2024-08-01"]),
    date_to: date = Query(examples=["2024-08-20"]),
    # title: str | None = Query(None, description='Название номера'),
    # description: str | None = Query(None, description='Описание номера'),
    # price_ge: int | None = Query(
    #     None, description='Цена больше или равна чем', ge=0),
    # price_le: int | None = Query(
    #     None, description='Цена меньше или равна чем', ge=0),
    # quantity: int | None = Query(None, description='Количество номеров', ge=0),
):
    if date_from > date_to:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Дата заезда позже даты выезда')
    per_page = pagination.per_page or 5
    rooms = await db.rooms.get_filtered_by_time(
        limit=per_page,
        offset=per_page * (pagination.page - 1),
        # title=title,
        # description=description,
        # price_ge=price_ge,
        # price_le=price_le,
        # quantity=quantity,
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )
    return rooms


@router.post("/{hotel_id}/rooms")
async def add_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс",
                    "description": "Дорогой люкс",
                    "price": 1000,
                    "quantity": 3,
                    "facilities_ids": [],
                },
            },
            "2": {
                "summary": "Обычный",
                "value": {
                    "title": "Обычный",
                    "description": "Обычный номер",
                    "price": 100,
                    "quantity": 3,
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFountException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Отель не найден')

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.add(data=_room_data)

    if room_data.facilities_ids:
        rooms_facilites_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
            for facility_id in room_data.facilities_ids
        ]
        await db.rooms_facilities.add_bulk(rooms_facilites_data)

    await db.commit()
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try: 
        return await db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
    except ObjectNotFountException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер не найдена')


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int) -> StatusOK:
    try:
        room = await db.rooms.get_one(id=room_id)
        if room.hotel_id != hotel_id:
            raise ObjectNotFountException
    except ObjectNotFountException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер не найден')

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return StatusOK


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest) -> StatusOK:
    try:
        room = await db.rooms.get_one(id=room_id)
        if room.hotel_id != hotel_id:
            raise ObjectNotFountException
    except ObjectNotFountException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер не найден')

    _room_data = RoomAdd(hotel_id=hotel_id, room_id=room_id, **room_data.model_dump())
    await db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)

    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )

    await db.commit()
    return StatusOK


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
) -> StatusOK:
    try:
        room = await db.rooms.get_one(id=room_id)
        if room.hotel_id != hotel_id:
            raise ObjectNotFountException
    except ObjectNotFountException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер не найден')
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, id=room_id, **_room_data_dict)
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )

    await db.commit()
    return StatusOK
