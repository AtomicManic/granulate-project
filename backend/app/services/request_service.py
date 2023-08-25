from uuid import UUID
from typing import Dict
from app.models.request_model import InsightRequest, TempRequest
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError
from pymongo import DESCENDING


class RequestService:
    @staticmethod
    async def save_suggestion(data: Dict, user_id: str):

        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing file data"
            )

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing user id"
            )
        sugg_in = InsightRequest(
            user_id=user_id,
            file_id=data["id"],
            data=data
        )
        print(sugg_in.file_id)
        new_sugg = await sugg_in.insert()

        return new_sugg

    @staticmethod
    async def save_temp_suggestion(data: Dict, user_id: str):
        print(user_id)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing file data"
            )

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing user id"
            )

        sugg_in = TempRequest(
            user_id=user_id,
            file_id=data["id"],
            data=data
        )
        print(type(sugg_in))
        try:
            new_sugg = await sugg_in.insert()
            return new_sugg
        except DuplicateKeyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="file already exist"
            )

    @staticmethod
    async def get_temp_by_id(user_id: UUID):
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing user id to fetch file"
            )
        suggestion = await TempRequest.find_one({"user_id": user_id})
        return suggestion

    @staticmethod
    async def get_request_by_file_id(file_id: str):
        document = await InsightRequest.find_one(InsightRequest.file_id == file_id)
        return document

    @staticmethod
    async def get_temp_request_by_file_id(file_id: str):
        document = await TempRequest.find_one(TempRequest.file_id == file_id)
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
