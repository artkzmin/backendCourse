from src.services.base import BaseService
from src.schemas.facilities import FacilityAdd, Facility
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def add_facility(self, data: FacilityAdd) -> Facility:
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return facility

    async def get_all(self) -> list[Facility]:
        return await self.db.facilities.get_all()
