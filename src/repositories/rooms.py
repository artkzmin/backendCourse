from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
        self,
        limit,
        offset,
        title,
        description,
        price_ge,
        price_le,
        quantity,
        hotel_id
    ) -> list[Room]:
        query = select(
            self.model
        )

        if title:
            query = (
                query
                .filter(func.lower(self.model.title).contains(title.strip().lower()))
            )
        if description:
            query = (
                query
                .filter(func.lower(self.model.description).contains(description.strip().lower()))
            )
        if price_ge:
            query = (
                query
                .filter(self.model.price >= price_ge)
            )
        if price_le:
            query = (
                query
                .filter(self.model.price <= price_le)
            )
        if hotel_id:
            query = (
                query
                .filter_by(hotel_id=hotel_id)
            )
        if quantity:
            query = (
                query
                .filter_by(quantity=quantity)
            )

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        rooms = await self.session.execute(query)

        return [
            self.schema.model_validate(model) for model in rooms.scalars().all()
        ]
