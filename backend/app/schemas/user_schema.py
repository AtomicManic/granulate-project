from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class UserAuth(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(..., max_length=50, min_length=2)
    last_name: str = Field(..., max_length=50, min_length=2)
    password: str = Field(..., min_length=8, max_length=24)


class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserNotFound(BaseModel):
    user: bool
