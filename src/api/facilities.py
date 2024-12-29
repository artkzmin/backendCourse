from fastapi import APIRouter, Body
from src.schemas.facilities import Facility, FacilityAdd
from src.api.dependencies import DBDep


router = APIRouter(
    prefix='/facilities',
    tags=['Удобства']
)


@router.get('/')
async def get_facilities(db: DBDep) -> list[Facility]:
    return await db.facilities.get_all()


@router.post('/')
async def create_facilities(db: DBDep, facility: FacilityAdd = Body()):
    facility = await db.facilities.add(facility)
    await db.commit()
    return {
        'status': 'OK',
        'data': facility
    }
