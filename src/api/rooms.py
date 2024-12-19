from fastapi import APIRouter, Query, Body
from datetime import date
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.rooms import Room, RoomAddRequest, RoomPatchRequest, RoomAdd, RoomPatch
from src.schemas.base import StatusOK

router = APIRouter(
    prefix='/hotels',
    tags=['Номера']
)


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    pagination: PaginationDep,
    date_from: date = Query(example='2024-08-01'),
    date_to: date = Query(example='2024-08-20')
    # title: str | None = Query(None, description='Название номера'),
    # description: str | None = Query(None, description='Описание номера'),
    # price_ge: int | None = Query(
    #     None, description='Цена больше или равна чем', ge=0),
    # price_le: int | None = Query(
    #     None, description='Цена меньше или равна чем', ge=0),
    # quantity: int | None = Query(None, description='Количество номеров', ge=0),
) -> list[Room]:
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
        date_to=date_to
    )
    return rooms


@router.post('/{hotel_id}/rooms')
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            '1': {
                'summary': 'Люкс',
                'value': {
                    'title': 'Люкс',
                    'description': 'Дорогой люкс',
                    'price': 1000,
                    'quantity': 3
                }
            },
            '2': {
                'summary': 'Обычный',
                'value': {
                    'title': 'Обычный',
                    'description': 'Обычный номер',
                    'price': 100,
                    'quantity': 3
                }
            }
        }
    )
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room_data = await db.rooms.add(data=_room_data)
    await db.commit()
    return {
        'status': 'OK',
        'data': room_data
    }


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int
) -> Room | None:
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    return room


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int
) -> StatusOK:
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return StatusOK


@router.put('/{hotel_id}/rooms/{room_id}')
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest
) -> StatusOK:
    _room_data = RoomAdd(hotel_id=hotel_id, room_id=room_id,
                         **room_data.model_dump())
    await db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return StatusOK


@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest
) -> StatusOK:
    _room_data = RoomPatch(
        hotel_id=hotel_id, id=room_id, **room_data.model_dump(exclude_unset=True)
    )
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return StatusOK
