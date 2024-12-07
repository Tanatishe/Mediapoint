from sqlalchemy.ext.asyncio import create_async_engine
from src.app.settings.config import settings


async_engine = create_async_engine(settings.db_dsn, echo=settings.app_env == "dev")
