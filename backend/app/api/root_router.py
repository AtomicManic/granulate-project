from fastapi import APIRouter
from app.api.auth_router import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
