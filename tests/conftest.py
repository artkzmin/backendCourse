# ruff: noqa: E402 F403
from dotenv import load_dotenv

load_dotenv(".test.env", override=True)

from unittest import mock


# мок кэша без лямбды
# def empty_cache(*args, **kwargs):
#     def wrapper(func):
#         return func

#     return wrapper


# mock.patch("fastapi_cache.decorator.cache", empty_cache).start()

# мок кэша с лямбдой
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import json
import pytest
from httpx import AsyncClient
from unittest import mock


from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


from src.main import app
from src.config import settings
from src.database import BaseOrm, engine_null_pool
from src.models import *
from src.api.dependencies import get_db


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function", autouse=True)
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    # async with app.router.lifespan_context(
    #     app
    # ):  # управляет жизненным циклом FastAPI, строка для работы кэша
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    print("Я ФИКСТУРА")
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    with open("tests/mock_user.json", encoding="utf-8") as f:
        user = json.load(f)
        print(user)
    await ac.post("/auth/register", json=user)


@pytest.fixture(scope="session")
async def authenticated_ac(ac, register_user) -> AsyncClient:
    with open("tests/mock_user.json", encoding="utf-8") as f:
        user = json.load(f)
    response = await ac.post("/auth/login", json=user)
    assert response.status_code == 200
    assert ac.cookies["access_token"]
    assert isinstance(ac.cookies["access_token"], str)
    # print(f'ACCESS_TOKEN={ac.cookies["access_token"]}')
    yield ac


# @pytest.fixture(scope="session", autouse=True)
# async def test_login(test_root):
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         await ac.post("/login", json={"email": "test@test.com", "password": "1234"})


@pytest.fixture(scope="session", autouse=True)
async def create_hotels(setup_database):
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
