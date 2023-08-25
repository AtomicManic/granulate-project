from fastapi import APIRouter, Depends, HTTPException, status, Body, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from jose import jwt
from pydantic import ValidationError
from uuid import UUID, uuid4

from app.services.user_service import UserService
from app.schemas.auth_schema import TokenSchema
from app.schemas.user_schema import UserOut
from app.models.user_model import User
from app.services.config import settings
from app.schemas.auth_schema import TokenPayload

from app.util.security import create_access_token, create_refresh_token
from app.api.deps.user_deps import get_current_user
from app.controller.jwt_controller import JWTController

router = APIRouter()


@router.post('/login', response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    response = await JWTController.login(form_data.username, form_data.password)
    return response


@router.post('/refresh', response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    response = await JWTController.refresh_token(refresh_token=refresh_token)
    return response


@router.get('/cookie')
async def get_cookie(request: Request, response: Response):
    print('cookie')
    cookie = request.cookies.get('anonymous_id')
    response = await JWTController.get_cookie(cookie, response)
