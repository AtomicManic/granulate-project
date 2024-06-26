from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_KEY: str = config("JWT_REFRESH_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "Cloud Opt"
    MONGO_DB_NAME: str = config("MONGO_DB_NAME", cast=str)

    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_DB_CONN_URL", cast=str)

    class Config:
        case_sensitive = True


settings = Settings()
