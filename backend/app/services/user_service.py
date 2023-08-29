from typing import Optional
from pymongo.errors import OperationFailure

from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.util.security import get_password, verify_password
from app.errors.errors import UnableToCreate


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = User(
            email=user.email,
            hashed_password=get_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name
        )
        try:
            await user_in.insert()
        except OperationFailure:
            raise UnableToCreate("user")

        new_user = await User.find_one(User.email == user.email)
        if not new_user:
            return None
        return new_user

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        if not user:
            return None
        return user

    @staticmethod
    async def get_user_by_id(id: str) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        if not user:
            return None
        return user
