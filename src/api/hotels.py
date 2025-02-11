from fastapi import APIRouter, Query, Body
from fastapi_cache.decorator import cache
from datetime import date
from src.schemas.hotels import HotelPatch, HotelAdd, Hotel
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.base import StatusOK


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(examples=["2024-08-01"]),
    date_to: date = Query(examples=["2024-08-20"]),
    title: str | None = Query(None, description="Заголовок отеля"),
    location: str | None = Query(None, description="Местоположение отеля"),
) -> list[Hotel]:

    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int) -> Hotel | None:
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
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
    hotel = await db.hotels.add(hotel_data)

    # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
    # Для дебага запроса:
    # from src.database import engine
    # print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
    # await session.execute(add_hotel_stmt)

    await db.commit()

    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int) -> StatusOK:
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return StatusOK


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd) -> StatusOK:
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return StatusOK


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновления данных об отеле",
    description="<h1>Подробное описание</h1>",
)
async def partially_edit_hotel(
    db: DBDep, hotel_id: int, hotel_data: HotelPatch
) -> StatusOK:
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return StatusOK
