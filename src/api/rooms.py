from fastapi import APIRouter, Query, Body
from datetime import date
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, Room
from src.schemas.base import StatusOK
from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
)
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    pagination: PaginationDep,
    date_from: date = Query(examples=["2024-08-01"]),
    date_to: date = Query(examples=["2024-08-20"]),
) -> list[Room]:
    rooms = await RoomService(db).get_filtered_by_time(
        pagination=pagination,
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
        room = await RoomService(db).add_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_one_or_none(room_id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int) -> StatusOK:
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise HotelNotFoundHTTPException
    return StatusOK


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest) -> StatusOK:
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return StatusOK


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
) -> StatusOK:
    try:
        await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return StatusOK
