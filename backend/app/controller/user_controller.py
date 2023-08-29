from pymongo.errors import DuplicateKeyError

from app.schemas.user_schema import UserAuth
from app.services.user_service import UserService
from app.errors.errors import DuplicateEntity


class UserController:
    @staticmethod
    async def register(data: UserAuth):
        try:
            registered = await UserService.create_user(data)
            return registered
        except DuplicateKeyError:
            raise DuplicateEntity("Email")
