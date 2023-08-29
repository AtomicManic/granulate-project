from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime
from pydantic import ValidationError

from app.models.user_model import User
from app.schemas.auth_schema import TokenPayload
from app.services.config import settings
from app.services.user_service import UserService

reusable_auth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_auth)) -> User:

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[settings.ALGORITHM])

        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expires",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authentication": "Bearer"}
        )

    user = await UserService.get_user_by_id(id=str(token_data.sub))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
            headers={"WWW-Authentication": "Bearer"}
        )
    return user
