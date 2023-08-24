from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
import pymongo
from uuid import uuid4
from jose import jwt
from typing import Union

from app.schemas.user_schema import UserAuth, UserOut, UserUpdate, UserNotFound
from app.services.user_service import UserService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.services.config import settings


class UserController:
    @staticmethod
    async def register(data: UserAuth):
        try:
            registered = await UserService.create_user(data)
            return registered
        except pymongo.errors.DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exist"
            )

    @staticmethod
    async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
        try:
            return await UserService.update_user(user.user_id, data)
        except pymongo.errors.OperationFailure:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist"
            )

    @staticmethod
    async def get_user(request: Request):
        token = request.cookies.get('anonymous_id')
        user = jwt.decode(token, settings.JWT_SECRET_KEY,
                          algorithms=settings.ALGORITHM)
        id = user["user_id"]
        current_user = await UserService.get_user_by_id(id=id)
        if (current_user):
            return current_user
        else:
            return {'user': False}
