from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAdd, Facility
from src.api.dependencies import DBDep
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep) -> list[Facility]:
    return await FacilityService(db).get_all()


@router.post("")
async def add_facilities(db: DBDep, facility: FacilityAdd = Body()):
    facility = await FacilityService(db).add_facility(facility)
    return {"status": "OK", "data": facility}
