import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


import uvicorn
import logging
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
from contextlib import asynccontextmanager


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.init import redis_manager


logging.basicConfig(level=logging.DEBUG)


# -------------------------------
# import asyncio
# from src.api.dependencies import get_db


# async def send_emails_bookings_today_checkin():
#     async for db in get_db():
#         bookings = await db.bookings.get_bookings_with_today_checkin()
#         print(f"{bookings=}")


# async def run_send_email_regularly():
#     while True:
#         await send_emails_bookings_today_checkin()
#         await asyncio.sleep(5)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # При старте приложения
#     asyncio.create_task(run_send_email_regularly())
#     await redis_manager.connect()
#     FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
#     yield
# -------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info('FastAPI cache initialized')
    yield
    # При выключени/перезагрузке приложения
    await redis_manager.close()


app = FastAPI(docs_url=None, lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
