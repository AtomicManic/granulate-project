from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from jose import jwt
from pydantic import ValidationError

from app.services.user_service import UserService
from app.schemas.auth_schema import TokenSchema
from app.schemas.user_schema import UserOut
from app.models.user_model import User
from app.services.config import settings
from app.schemas.auth_schema import TokenPayload

from app.util.security import create_access_token, create_refresh_token
from app.api.deps.user_deps import get_current_user

router = APIRouter()


@router.post('/login', response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }


@router.post('/test-token', response_model=UserOut)
async def test_token_validity(user: User = Depends(get_current_user)):
    return user


@router.post('/refresh', response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_KEY, algorithms=[
                settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user"
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }
