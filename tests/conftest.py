from dotenv import load_dotenv
import json

from src.schemas.rooms import RoomAddRequest

load_dotenv(".test.env", override=True)

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
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/mock_hotels.json") as f:
            hotels = json.load(f)
            for h in hotels:
                print(h)
                await ac.post("/hotels", json=h)


@pytest.fixture(scope="session", autouse=True)
async def create_rooms(create_hotels):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/mock_rooms.json") as f:
            rooms = json.load(f)
            for r in rooms:
                r_add = RoomAddRequest(**r)
                url = f"/hotels/{r['hotel_id']}/rooms"
                print(url, r_add.model_dump())
                res = await ac.post(url, json=r_add.model_dump())
                print(res)
