from fastapi import APIRouter, Query, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Заголовок отеля"),
        location: str | None = Query(None, description="Местоположение отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )
    


@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post('')
async def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        '1': {
            'summary': 'Сочи',
            'value': {
                'title': 'Отель Сочи',
                'location': 'Ул. Морская, 1'
            }
        },
        '2': {
            'summary': 'Дубай',
            'value': {
                'title': 'Отель Дубай',
                'location': 'Ул. Шейха, 2'
            }
        }
    })
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)

        # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # Для дебага запроса:
        # from src.database import engine
        # print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        # await session.execute(add_hotel_stmt)

        await session.commit()

    return {'status': 'OK', 'data': hotel}


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {
        'status': 'OK'
    }


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, id=hotel_id)
        await session.commit()
    return {
        'status': 'OK'
    }


@router.patch(
    "/{hotel_id}",
    summary='Частичное обновления данных об отеле',
    description='<h1>Подробное описание</h1>'
)
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {
        'status': 'OK'
    }
