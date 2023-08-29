from uuid import uuid4
import aiofiles
import json
from fastapi import HTTPException


class IntelMockService:
    @staticmethod
    def get_insight_id(data: dict):
        return f"{uuid4()}"

    @staticmethod
    async def get_insights(data: dict, insight_id: str):
        try:
            async with aiofiles.open('app/data/output.json', mode="r") as file:
                data = await file.read()
            return json.loads(data)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="Failed to parse JSON file")
