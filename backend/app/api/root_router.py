from fastapi import APIRouter

from app.api.user_router import router as user_router
from app.api.jwt_router import router as jwt_router

router = APIRouter()

router.include_router(user_router, prefix="/users")
router.include_router(jwt_router, prefix="/auth")
