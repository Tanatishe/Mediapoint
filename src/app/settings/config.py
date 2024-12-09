from dynaconf import Dynaconf
from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from loguru import logger

_settings = Dynaconf(settings_files=["config.yaml"])


logger.add('logs/logs.log', level='DEBUG')
logger.debug('Error')
logger.info('Information message')
logger.warning('Warning')


_db_dsn = AnyUrl.build(
    scheme="postgresql+asyncpg",
    username=_settings.database.user,
    password=_settings.database.password,
    host=_settings.database.host,
    port=_settings.database.port,
    path=_settings.database.db,
)


class Settings(BaseSettings):
    app_name: str
    app_env: str
    db_dsn: str
    kafka_topic: str
    kafka_key: str
    first_external_host: str
    second_external_host: str


settings = Settings(
    app_name=_settings.app_name,
    app_env=_settings.app_env,
    db_dsn=str(_db_dsn),
    kafka_topic=_settings.kafka_topic,
    kafka_key=_settings.kafka_key,
    first_external_host=_settings.first_external_host,
    second_external_host=_settings.second_external_host,
)
