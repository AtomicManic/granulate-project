from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(..., max_length=50, min_length=2)
    last_name: str = Field(..., max_length=50, min_length=2)
    password: str = Field(..., min_length=8, max_length=24)
