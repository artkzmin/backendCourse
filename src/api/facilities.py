from fastapi import APIRouter
from src.schemas.facilities import Facilities, FacilitiesAdd
from src.api.dependencies import DBDep


router = APIRouter(
    prefix='/facilities',
    tags=['Удобства']
)


@router.get('/')
async def get_facilities(db: DBDep) -> list[Facilities]:
    return await db.facilities.get_all()


@router.post('/')
async def create_facilities(obj: FacilitiesAdd, db: DBDep):
    facility = await db.facilities.add(obj)
    await db.commit()
    return {
        'status': 'OK',
        'data': facility
    }
