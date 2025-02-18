from datetime import date

from src.services.base import BaseService
from src.exceptions import (
    check_date_to_after_date_from,
    HotelNotFoundException,
    ObjectNotFoundException,
)
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        date_from: date,
        date_to: date,
        title: str | None = None,
        location: str | None = None,
    ) -> list[Hotel]:
        check_date_to_after_date_from(date_from=date_from, date_to=date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int) -> Hotel:
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAdd) -> Hotel:
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int) -> None:
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd) -> None:
        await self.db.hotels.edit(data=hotel_data, id=hotel_id)
        await self.db.commit()

    async def partially_edit_hotel(self, hotel_id: int, hotel_data: HotelPatch) -> None:
        await self.db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
