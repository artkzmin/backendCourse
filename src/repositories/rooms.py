from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomWithRels
from src.repositories.utils import rooms_ids_for_booking

from sqlalchemy import select
from sqlalchemy.orm import selectinload


class RoomsRepository(BaseRepository):
    model: RoomsOrm = RoomsOrm
    schema = Room

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model)

    async def get_filtered_by_time(
        self,
        limit,
        offset,
        hotel_id,
        date_from,
        date_to
    ):

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [RoomWithRels.model_validate(model) for model in result.unique().scalars().all()]
