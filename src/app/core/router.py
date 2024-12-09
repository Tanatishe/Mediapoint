from src.app.settings.config import logger
from fastapi import APIRouter, Depends, HTTPException

from src.app.core.service import post_request, get_request, kafka_send
from src.app.settings.dto import DataRequest

router = APIRouter(prefix="/data", tags=["data"])


@router.post("")
async def post_data(request: DataRequest) -> dict:
    try:
        data = request.content
        response = await post_request(data)
    except Exception as e:
        logger.error(f"v poste {repr(e)}")
        raise HTTPException(400, detail="Bad Request")
    else:
        await kafka_send(data)
        return {
            "id": int(response.all()[0][0]),
            "message": "Data saved and published to Kafka.",
        }


@router.get("")
async def get_data(entries=Depends(get_request)) -> list:
    return [
        {
            "id": entry.id,
            "content": entry.content.get("content"),
            "created_at": entry.created_at.isoformat(timespec="seconds"),
        }
        for entry in entries
    ]
