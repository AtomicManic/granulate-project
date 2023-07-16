from fastapi import FastAPI
from app.services.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user_model import User
from app.api.root_router import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """

    # DB Client
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)

    # DB Name
    db = db_client.get_database(settings.MONGO_DB_NAME)

    await init_beanie(
        database=db,
        document_models=[
            User
        ]
    )

app.include_router(router, prefix=settings.API_V1_STR)
