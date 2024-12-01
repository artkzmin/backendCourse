from fastapi import APIRouter, Query, Body
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        id: int | None = Query(None, description="ID"),
        title: str | None = Query(None, description="Заголовок отеля"),
        page: int = Query(1, description="Номер страницы"),
        per_page: int = Query(
            3, description="Количество отелей на одной странице"
        )
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_[(page-1)*per_page:page*(per_page)]


@router.post('')
def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        '1': {
            'summary': 'Сочи',
            'value': {
                'title': 'Отель Сочи',
                'name': 'Сочи у моря'
            }
        },
        '2': {
            'summary': 'Дубай',
            'value': {
                'title': 'Отель Дубай',
                'name': 'Дубай у фонтана'
            }
        }
    })
):
    global hotels
    hotels.append(
        {
            'id': hotels[-1]['id'] + 1,
            'title': hotel_data.title,
            'name': hotel_data.name
        }
    )
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
