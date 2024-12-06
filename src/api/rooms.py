from fastapi import APIRouter, Query
from src.api.dependencies import PaginationDep
from src.schemas.rooms import Room, RoomAdd, RoomPATCH
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.base import StatusOK

router = APIRouter(
    prefix='/rooms',
    tags=['Номера отелей']
)


@router.get('')
async def get_rooms(
    pagination: PaginationDep,
    title: str | None = Query(None, description='Название номера'),
    description: str | None = Query(None, description='Описание номера'),
    price_ge: int | None = Query(
        None, description='Цена больше или равна чем', ge=0),
    price_le: int | None = Query(
        None, description='Цена меньше или равна чем', ge=0),
    quantity: int | None = Query(None, description='Количество номеров', ge=0),
    hotel_id: int | None = Query(None, description='ID отеля', ge=0)
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


@router.post('')
async def add_rooms(
    room: RoomAdd
) -> Room:
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(data=room)
        await session.commit()
        return room


@router.get('{room_id}')
async def get_room(
    room_id: int
) -> Room | None:
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        return room


@router.delete('{room_id}')
async def delete_room(
    room_id: int
) -> StatusOK:
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return StatusOK


@router.put('{room_id}')
async def edit_room(
    room_id: int,
    room: RoomAdd
) -> StatusOK:
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room, id=room_id)
        await session.commit()
    return StatusOK


@router.patch('{room_id}')
async def partially_edit_room(
    room_id: int,
    room: RoomPATCH
) -> StatusOK:
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room, exclude_unset=True, id=room_id)
        await session.commit()
    return StatusOK
