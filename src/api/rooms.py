from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep
from src.schemas.rooms import Room, RoomAddRequest, RoomPatchRequest, RoomAdd, RoomPatch
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.base import StatusOK

router = APIRouter(
    prefix='/hotels',
    tags=['Номера']
)


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int,
    pagination: PaginationDep,
    title: str | None = Query(None, description='Название номера'),
    description: str | None = Query(None, description='Описание номера'),
    price_ge: int | None = Query(
        None, description='Цена больше или равна чем', ge=0),
    price_le: int | None = Query(
        None, description='Цена меньше или равна чем', ge=0),
    quantity: int | None = Query(None, description='Количество номеров', ge=0),
) -> list[Room]:
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:

        rooms = await RoomsRepository(session).get_all(
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            title=title,
            description=description,
            price_ge=price_ge,
            price_le=price_le,
            quantity=quantity,
            hotel_id=hotel_id
        )
        return rooms


@router.post('/{hotel_id}/rooms')
async def create_room(
    hotel_id: int,
    room_data: RoomAddRequest = Body()
) -> Room:
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room_data = await RoomsRepository(session).add(data=_room_data)
        await session.commit()
        return room_data


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(
    hotel_id: int,
    room_id: int
) -> Room | None:
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        return room


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    hotel_id: int,
    room_id: int
) -> StatusOK:
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return StatusOK


@router.put('/{hotel_id}/rooms/{room_id}')
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest
) -> StatusOK:
    _room_data = RoomAdd(hotel_id=hotel_id, room_id=room_id,
                         **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=_room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return StatusOK


@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest
) -> StatusOK:
    _room_data = RoomPatch(
        hotel_id=hotel_id, id=room_id, **room_data.model_dump(exclude_unset=True)
    )
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return StatusOK
