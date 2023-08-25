from uuid import UUID
from typing import Dict
from app.models.request_model import InsightRequest, TempRequest
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError


class RequestService:
    @staticmethod
    async def save_suggestion(data: Dict, user_id: UUID):
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
        new_sugg = await sugg_in.insert()
        return new_sugg

    @staticmethod
    async def save_temp_suggestion(data: Dict, user_id: UUID):
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
