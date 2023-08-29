from typing import Dict
from pymongo import DESCENDING

from app.models.request_model import InsightRequest, TempRequest


class RequestService:
    @staticmethod
    async def save_suggestion(data: Dict, user_id: str, insights: Dict):

        sugg_in = InsightRequest(
            user_id=user_id,
            file_id=data["id"],
            data=data,
            insights=insights
        )
        new_sugg = await sugg_in.insert()
        if not new_sugg:
            return None

        return new_sugg

    @staticmethod
    async def save_temp_suggestion(data: Dict, user_id: str, insights):
        sugg_in = TempRequest(
            user_id=user_id,
            file_id=data["id"],
            data=data,
            insights=insights
        )

        new_sugg = await sugg_in.insert()
        if not new_sugg:
            return None
        return new_sugg

    @staticmethod
    async def get_request_by_file_id(file_id: str):
        document = await InsightRequest.find_one(InsightRequest.file_id == file_id)
        if not document:
            return None
        return document

    @staticmethod
    async def get_temp_request_by_file_id(file_id: str):
        document = await TempRequest.find_one(TempRequest.file_id == file_id)
        if not document:
            return None
        return document

    @staticmethod
    async def get_insights_by_user_id(user_id: str):
        motor_collection = InsightRequest.get_motor_collection()
        cursor = motor_collection.find(
            {'user_id': user_id},
            {'_id': 0, 'created_at': 1, 'insights': 1}
        ).sort('created_at', DESCENDING)
        sorted_documents = await cursor.to_list(length=100)

        return sorted_documents
