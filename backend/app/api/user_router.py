from fastapi import APIRouter, HTTPException, status, Depends
import pymongo

from app.schemas.user_schema import UserAuth, UserOut, UserUpdate
from app.services.user_service import UserService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

router = APIRouter()


@router.post('/register', response_model=UserOut)
async def register(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist"
        )


@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.post('/update', summary='Update User', response_model=UserOut)
async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
    try:
        return await UserService.update_user(user.user_id, data)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
