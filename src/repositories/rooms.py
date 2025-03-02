from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRealsMapper
from src.schemas.rooms import Room
from src.exceptions import RoomNotFoundException


class RoomsRepository(BaseRepository):
    model: RoomsOrm = RoomsOrm
    mapper: RoomDataMapper = RoomDataMapper

    async def get_one_or_none_with_rels(self, **filter_by) -> Room | None:
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomDataWithRealsMapper.map_to_domain_entity(model)

    async def get_one_with_rels(self, **filter_by) -> Room:
        result = await self.get_one_or_none_with_rels(**filter_by)
        if not result:
            raise RoomNotFoundException

        return result

    async def get_filtered_by_time(self, limit, offset, hotel_id, date_from, date_to):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [
            RoomDataWithRealsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]
