from dotenv import load_dotenv

load_dotenv(".test.env", override=True)

import json

from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


from src.main import app
from httpx import AsyncClient

import pytest
from src.config import settings
from src.database import BaseOrm, engine_null_pool
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    print("Я ФИКСТУРА")
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def test_root(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register", json={"email": "test@test.com", "password": "1234"}
        )


@pytest.fixture(scope="session", autouse=True)
async def test_login(test_root):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/login", json={"email": "test@test.com", "password": "1234"})


@pytest.fixture(scope="session", autouse=True)
async def create_hotels(test_login):
    with open("tests/mock_hotels.json", encoding="utf-8") as f:
        hotels = json.load(f)
    hotels = [HotelAdd.model_validate(h) for h in hotels]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def create_rooms(create_hotels):
    with open("tests/mock_rooms.json", encoding="utf-8") as f:
        rooms = json.load(f)
    rooms = [RoomAdd.model_validate(r) for r in rooms]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.rooms.add_bulk(rooms)
        await db.commit()
