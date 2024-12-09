from fastapi import FastAPI

from src.app.settings.config import settings
from src.app.core.router import router as api_router


def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        docs_url="/docs" if settings.app_env == "dev" else None,
    )
    app.include_router(api_router)

    return app
