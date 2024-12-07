import json
from fastapi import HTTPException, Depends
from src.app.core.kafka import send_one
from src.app.database.database import async_engine

from sqlalchemy import text


async def create_db():
    async with async_engine.connect() as conn:
        try:
            request = "CREATE TABLE if not exists data_entries (id SERIAL PRIMARY KEY, content JSONB NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            await conn.execute(text(request))
        except Exception as e:
            raise HTTPException(400, detail=repr(e))
        else:
            await conn.commit()


async def base_request(request: text):
    await create_db()
    async with async_engine.connect() as conn:
        try:
            response = await conn.execute(request)
        except Exception as e:
            raise HTTPException(400, detail=repr(e))
        else:
            await conn.commit()
            return response


async def post_request(data: str):
    response = await base_request(
        text(
            "insert into data_entries (content) values ('%s') returning id"
            % (json.dumps({"content": data}))
        )
    )
    await send_one(data)
    return response


async def get_request():
    return await base_request(text("select * from data_entries"))
