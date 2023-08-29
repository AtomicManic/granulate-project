from fastapi import APIRouter, Depends

from app.schemas.user_schema import UserAuth, UserOut
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.controller.user_controller import UserController

router = APIRouter()


@router.post('/register', response_model=UserOut)
async def register(data: UserAuth):
    registered = await UserController.register(data)
    return registered


@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user
