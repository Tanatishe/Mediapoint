from fastapi import APIRouter, Depends

from src.app.core.service import post_request, get_request
from src.app.settings.dto import DataRequest

router = APIRouter(prefix="/data", tags=["data"])


@router.post("")
async def post_data(request: DataRequest):
    try:
        response = await post_request(request.content)
    except Exception as e:
        return repr(e)
    else:
        return {
            "id": int(response.all()[0][0]),
            "message": "Data saved and published to Kafka.",
        }


@router.get("")
async def get_data(entries=Depends(get_request)):
    return [
        {
            "id": entry.id,
            "content": entry.content.get("content"),
            "created_at": entry.created_at.isoformat(timespec="seconds"),
        }
        for entry in entries
    ]
