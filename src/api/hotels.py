from fastapi import APIRouter, Query, Body
from fastapi_cache.decorator import cache
from datetime import date
from src.schemas.hotels import HotelPatch, HotelAdd, Hotel
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.base import StatusOK
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.services.hotels import HotelService


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query("2024-08-01"),
    date_to: date = Query("2024-08-20"),
    title: str | None = Query(None, description="Заголовок отеля"),
    location: str | None = Query(None, description="Местоположение отеля"),
) -> list[Hotel]:
    return await HotelService(db).get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        pagination=pagination,
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int) -> Hotel:
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def add_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Отель Сочи", "location": "Ул. Морская, 1"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Отель Дубай", "location": "Ул. Шейха, 2"},
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)

    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int) -> StatusOK:
    await HotelService(db).delete_hotel(hotel_id)
    return StatusOK


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd) -> StatusOK:
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return StatusOK


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновления данных об отеле",
    description="<h1>Подробное описание</h1>",
)
async def partially_edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch) -> StatusOK:
    await HotelService(db).partially_edit_hotel(hotel_id, hotel_data)
    return StatusOK
