from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility

from pydantic import BaseModel
from sqlalchemy import insert, delete, select


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def edit_balk(self, room_id: int, facilities_ids: list[int]) -> None:

        delete_stmt = (
            delete(RoomsFacilitiesOrm)
            .filter_by(room_id=room_id)
            .filter(
                RoomsFacilitiesOrm.facility_id.not_in(facilities_ids)
            )
        )
        await self.session.execute(delete_stmt)
        old_ids_query = (
            select(RoomsFacilitiesOrm.facility_id)
            .filter_by(room_id=room_id)
        )
        old_ids = set(await self.session.execute(old_ids_query))
        to_add_ids = set(facilities_ids) - old_ids
        add_stmt = (
            insert(RoomsFacilitiesOrm)
            .values(
                [
                    {'room_id': room_id, 'facility_id': f_id}
                    for f_id in to_add_ids
                ]
            )
        )

        await self.session.execute(add_stmt)
