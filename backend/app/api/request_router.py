from fastapi import APIRouter, Request
import pymongo
from typing import Dict

from app.controller.request_controller import RequestController
router = APIRouter()


@router.post("")
async def save_suggestion(data: Dict, id: str, request: Request):
    if id:
        isAuth = True
        data = await RequestController.save_auth_request(data, id)
    else:
        isAuth = False
        data = await RequestController.save_temp_request(data, request)

    response = await RequestController.generate_insights(
        data, data.file_id, isAuth)
    return response


@router.get('/insights')
async def get_insights_by_user_id(id: str):
    print("45454")
    response = await RequestController.get_insights_by_user_id(id)
    return response
