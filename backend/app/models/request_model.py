from beanie import Document
from typing import Dict
from pydantic import Field
from datetime import datetime
from beanie.odm.fields import IndexModel
from pymongo import ASCENDING


class InsightRequest(Document):
    user_id: str
    file_id: str
    data: Dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "insight_requests"
        indexes = [
            IndexModel(keys=[("file_id", ASCENDING)], unique=True)
        ]


class TempRequest(Document):
    user_id: str
    file_id: str
    data: Dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "temporary_requests"
        indexes = [
            IndexModel(keys=[("file_id", ASCENDING)], unique=True)
        ]
