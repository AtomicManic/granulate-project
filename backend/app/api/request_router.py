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
        data.data['data'], isAuth, request, id)
    return {"data": response}
