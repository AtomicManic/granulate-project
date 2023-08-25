from fastapi import FastAPI
from app.services.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user_model import User
from app.models.request_model import InsightRequest, TempRequest
from app.api.root_router import router
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_handler_mw import exception_middleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.middleware("http")(exception_middleware)

origins = [
    "http://localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
            User,
            InsightRequest,
            TempRequest
        ]
    )


app.include_router(router, prefix=settings.API_V1_STR)
