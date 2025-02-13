from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Удобства"])


# import json
# from src.init import redis_manager
# @router.get("/")
# async def get_facilities(db: DBDep):
#     facilities_from_cache = await redis_manager.get("facilities")
#     if not facilities_from_cache:
#         facilities = await db.facilities.get_all()
#         facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
#         facilities_json = json.dumps(facilities_schemas)
#         await redis_manager.set("facilities", facilities_json, 10)
#         return facilities
#     else:
#         facilities_dicts = json.loads(facilities_from_cache)
#         return facilities_dicts


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def create_facilities(db: DBDep, facility: FacilityAdd = Body()):
    facility = await db.facilities.add(facility)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facility}
