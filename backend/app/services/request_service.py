from uuid import UUID
from typing import Dict
from app.models.request_model import Request, TempRequest
from fastapi import HTTPException, status


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

        sugg_in = Request(
            user_id=user_id,
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
            data=data
        )
        new_sugg = await sugg_in.insert()
        return new_sugg

    @staticmethod
    async def get_temp_by_id(user_id: UUID):
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing user id to fetch file"
            )
        suggestion = await TempRequest.find_one({"user_id": user_id})
        return suggestion
