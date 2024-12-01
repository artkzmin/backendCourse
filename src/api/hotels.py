from fastapi import APIRouter, Query, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from sqlalchemy import insert, select, func
from src.models.hotels import HotelsOrm

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Заголовок отеля"),
        location: str | None = Query(None, description="Местоположение отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
                query
                .limit(per_page)
                .offset(per_page * (pagination.page - 1))
            )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())

        # Для дебага запроса:
        # from src.database import engine
        # print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'OK'}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {
        'status': 'OK'
    }


@router.put("/{hotel_id}")
def edit_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels
    hotel = [h for h in hotels if h['id'] == hotel_id][0]
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name
    return {
        'status': 'OK'
    }


@router.patch(
    "/{hotel_id}",
    summary='Частичное обновления данных об отеле',
    description='<h1>Подробное описание</h1>'
)
def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    global hotels
    hotel = [h for h in hotels if h['id'] == hotel_id][0]
    if hotel_data.title:
        hotel['title'] = hotel_data.title
    if hotel_data.name:
        hotel['name'] = hotel_data.name
    return {
        'status': 'OK'
    }
