import json
from fastapi import HTTPException
from src.app.settings.config import settings
from src.app.core.kafka import producer
from src.app.database.database import async_engine
from src.app.settings.config import logger

from sqlalchemy import CursorResult, text


async def create_db() -> None:
    async with async_engine.connect() as conn:
        try:
            request = "CREATE TABLE if not exists data_entries (id SERIAL PRIMARY KEY, content JSONB NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            await conn.execute(text(request))
        except Exception as e:
            logger.error(repr(e))
            raise HTTPException(400, detail="NO BASE")
        else:
            await conn.commit()


async def kafka_send(data: str) -> None:
    try:
        await producer.start()
        await producer.send(
            topic=settings.kafka_topic, 
            key=settings.kafka_key, 
            value=bytes(data)
        )
    except Exception as e:
        logger.error(repr(e))
    finally:
        await producer.stop()


async def base_request(request: text) -> CursorResult:
    await create_db()
    async with async_engine.connect() as conn:
        try:
            response = await conn.execute(request)
        except Exception as e:
            logger.error(repr(e))
            raise HTTPException(400, detail="very Bad Request")
        else:
            await conn.commit()
            return response


async def post_request(data: str) -> CursorResult:
    response = await base_request(
        text(
            "insert into data_entries (content) values ('%s') returning id"
            % (json.dumps({"content": data}))
        )
    )
    return response


async def get_request()-> CursorResult:
    return await base_request(text("select * from data_entries"))
