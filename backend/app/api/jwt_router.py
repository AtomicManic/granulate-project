from fastapi import APIRouter, Depends, Body, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from app.schemas.auth_schema import TokenSchema
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
    cookie = request.cookies.get('anonymous_id')
    response = await JWTController.get_cookie(cookie, response)
