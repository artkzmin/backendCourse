from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        limit,
        offset,
        hotel_id,
        date_from,
        date_to


    ) -> list[Room]:

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id
        )

        rooms_ids_to_get = (
            rooms_ids_to_get
            .limit(limit)
            .offset(offset)
        )

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
