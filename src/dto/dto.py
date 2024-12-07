
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, JSON, DateTime






class DataEntry(Base):
    __tablename__ = "data_entries"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DataRequest(BaseModel):
    content: str

class DataResponse(BaseModel):
    id: int
    message: str