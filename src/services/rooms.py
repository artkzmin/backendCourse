from datetime import date
from src.services.base import BaseService
from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    RoomNotFoundException,
)
from src.schemas.rooms import Room, RoomAddRequest, RoomAdd, RoomPatch, RoomPatchRequest
from src.schemas.facilities import RoomFacilityAdd
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
        self, hotel_id: int, pagination, date_from: date, date_to: date
    ) -> list[Room]:
        await check_date_to_after_date_from(date_from=date_from, date_to=date_to)

        per_page = pagination.per_page or 5
        rooms = await self.db.rooms.get_filtered_by_time(
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
        return rooms

    async def get_one_or_none(self, hotel_id: int, room_id: int) -> Room | None:
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def add_room(self, hotel_id: int, room_data: RoomAddRequest) -> Room:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        room = await self.db.rooms.add(data=_room_data)

        if room_data.facilities_ids:
            rooms_facilites_data = [
                RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
                for facility_id in room_data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilites_data)

        await self.db.commit()
        return room

    async def delete_room(self, hotel_id: int, room_id: int) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def edit_room(
        self, hotel_id: int, room_id: int, room_data: RoomAddRequest
    ) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room_data = RoomAdd(
            hotel_id=hotel_id, room_id=room_id, **room_data.model_dump()
        )
        await self.db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
        )
        await self.db.commit()

    async def partially_edit_room(
        self, hotel_id: int, room_id: int, room_data: RoomPatchRequest
    ) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, id=room_id, **_room_data_dict)
        await self.db.rooms.edit(
            data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )

        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )

        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
