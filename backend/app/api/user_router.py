from fastapi import APIRouter, HTTPException, status
import pymongo

from app.schemas.user_schema import UserAuth, UserOut
from app.services.user_service import UserService

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
