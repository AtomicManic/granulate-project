from fastapi import APIRouter, Request
from typing import Dict

from app.controller.request_controller import RequestController
from app.errors.errors import UnableToProcess, MissingAttribute, UnableToCreate

router = APIRouter()


@router.post("")
async def save_suggestion(data: Dict, id: str, request: Request):
    if not data:
        raise MissingAttribute("File data")

    if id == "invalid":
        raise UnableToProcess("user details")
    elif id:
        isAuth = True
        sugg = await RequestController.save_auth_request(data, id, isAuth)
    else:
        isAuth = False
        sugg = await RequestController.save_temp_request(data, request, isAuth)

    if not sugg:
        raise UnableToCreate("Request")

    return sugg


@router.get('/insights')
async def get_insights_by_user_id(id: str):
    response = await RequestController.get_insights_by_user_id(id)
    return response
