from sqlalchemy import select, func
from datetime import date

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset) -> list[Hotel]:
        query = select(self.model)
        if location:
            query = query.filter(func.lower(
                self.model.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(
                self.model.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to
        )

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        hotels_ids_filtered = (
            select(HotelsOrm.id)
            .select_from(HotelsOrm)
            .filter(HotelsOrm.id.in_(hotels_ids_to_get))
        )

        if location:
            hotels_ids_filtered = hotels_ids_filtered.filter(func.lower(
                HotelsOrm.location).contains(location.strip().lower()))
        if title:
            hotels_ids_filtered = hotels_ids_filtered.filter(func.lower(
                HotelsOrm.title).contains(title.strip().lower()))

        hotels_ids_filtered = (
            hotels_ids_filtered
            .limit(limit)
            .offset(offset)
        )

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_filtered))
