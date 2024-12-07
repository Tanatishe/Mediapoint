from pydantic import BaseModel


class DataRequest(BaseModel):
    content: str
