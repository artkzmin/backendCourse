import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.api.auth import router as auth_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(router_hotels)
app.include_router(rooms_router)
app.include_router(bookings_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='127.0.0.1', port=8000)
