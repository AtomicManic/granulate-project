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
from app.controller.user_controller import UserController

router = APIRouter()


@router.post('/register', response_model=UserOut)
async def register(data: UserAuth):
    registered = await UserController.register(data)
    return registered


@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.post('/update', summary='Update User', response_model=UserOut)
async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
    return await UserController.update_user(data, user)


@router.get('/user', response_model=Union[UserOut, UserNotFound])
async def get_user(request: Request):
    return await UserController.get_user(request)
