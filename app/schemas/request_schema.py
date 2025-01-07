import datetime
from pydantic import BaseModel
from typing import Optional


class RequestCreate(BaseModel):
    timestamp: datetime.datetime
    endpoint: str
    http_method: str
    status_code: int
    response_time: float
    request_size: int
    response_size: int
    
class RequestOutput(BaseModel):
    id: int
    timestamp: datetime.datetime
    endpoint: str
    http_method: str
    status_code: int
    response_time: float
    request_size: int
    response_size: int
    class Config:
        from_attributes = True