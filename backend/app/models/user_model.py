import datetime
from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field, EmailStr, field_validator
from email_validator import validate_email


class User(Document):
    user_id: UUID = Field(default_factory=lambda: str(uuid4()))
    email: Indexed(str, unique=True)
    hashed_password: str
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    def __repr__(self) -> str:
        return f"<User {self.email}"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @property
    def create(self) -> datetime:
        return self.id.generation_time
