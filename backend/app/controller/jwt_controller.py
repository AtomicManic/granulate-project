from fastapi import Body, Response
from jose import jwt
from uuid import uuid4
from pymongo.errors import OperationFailure

from app.services.user_service import UserService
from app.services.config import settings
from app.schemas.auth_schema import TokenPayload
from app.errors.errors import CookieNotFound, UnableToGet, MissingAttribute, UnAuthenticated, JWTDecodeError, EntityNotFound
from app.util.security import create_access_token, create_refresh_token


class JWTController:
    @staticmethod
    async def login(email, password):
        if not email:
            raise MissingAttribute("Email")

        if not password:
            raise MissingAttribute("Password")
        user = await UserService.authenticate(email=email, password=password)
        if not user:
            raise UnAuthenticated()

        return {
            "access_token": create_access_token(user.user_id),
            "refresh_token": create_refresh_token(user.user_id)
        }

    @staticmethod
    async def refresh_token(refresh_token: str = Body(...)):
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_REFRESH_KEY, algorithms=[
                    settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

            user = await UserService.get_user_by_id(token_data.sub)

            if not user:
                raise EntityNotFound("User")

            return {
                "access_token": create_access_token(user.user_id),
                "refresh_token": create_refresh_token(user.user_id)
            }

        except (jwt.JWTError):
            raise JWTDecodeError()
        except (OperationFailure):
            raise UnableToGet("user")

    @staticmethod
    async def get_cookie(cookie: str, response: Response):
        try:
            if not cookie:
                data = {"user_id": f"{uuid4()}"}
                token = jwt.encode(data, settings.JWT_SECRET_KEY,
                                   algorithm=settings.ALGORITHM)
                response.set_cookie(key="anonymous_id", value=token,
                                    httponly=True, max_age=1800, expires=1800, samesite="None", secure=True)
                return {"message": "cookie is set"}
            return {"message": "cookie exist"}
        except Exception as e:
            raise CookieNotFound()
