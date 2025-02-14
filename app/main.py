from typing import Annotated

from fastapi import Depends, FastAPI

from app.config import Settings, get_settings

app = FastAPI()

@app.get("/")
async def read_root(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "message": "Hello World",
        "app_name": settings.APP_TITLE,
        "app_version": settings.APP_VERSION,
    }
