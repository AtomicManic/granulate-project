from beanie import Document
from typing import Dict
from pydantic import Field
from datetime import datetime


class Request(Document):
    user_id: str
    data: Dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "requests"


class TempRequest(Document):
    user_id: str
    data: Dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "temporary_requests"
