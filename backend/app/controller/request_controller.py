from fastapi import Request
from typing import Dict
from jose import jwt, JWTError
from pymongo.errors import WriteError, DuplicateKeyError

from app.services.intel_mock_service import IntelMockService
from app.services.config import settings
from app.services.request_service import RequestService
from app.util.insights_analysis import InsightAnalysis
from app.models.request_model import InsightRequest
from app.errors.errors import EntityNotFound, JWTDecodeError, CookieNotFound, UnableToCreate, UnableToGet, MissingAttribute, DuplicateEntity


class RequestController:

    @staticmethod
    async def save_temp_request(data: Dict, request: Request, isAuth: bool):
        if not data["data"]:
            raise MissingAttribute("file")

        try:
            cookie = request.cookies.get("anonymous_id", None)
            if cookie is None:
                raise CookieNotFound()
            user = jwt.decode(
                cookie, settings.JWT_SECRET_KEY, settings.ALGORITHM)

            if not user['user_id']:
                raise MissingAttribute("user id")

            insights = await RequestController.generate_insights(data['data'], data['data']['id'], isAuth)
            if not insights:
                raise UnableToCreate("insights")

            new_data = await RequestService.save_temp_suggestion(data["data"], user_id=user['user_id'], insights=insights)
            if not new_data:
                raise UnableToCreate("request")
            return new_data

        except JWTError:
            raise JWTDecodeError()
        except DuplicateKeyError:
            raise DuplicateEntity("file")
        except WriteError:
            raise UnableToCreate("request")

    @staticmethod
    async def save_auth_request(data: Dict, id: str, isAuth: bool):
        if not data['data']:
            raise MissingAttribute("File data")
        if not id:
            raise MissingAttribute("User id")
        insights = await RequestController.generate_insights(data['data'], data['data']['id'], isAuth)
        if not insights:
            raise UnableToCreate("insights")
        try:
            new_data = await RequestService.save_suggestion(data=data["data"], user_id=id, insights=insights)
            if not new_data:
                raise UnableToCreate("request")
            return new_data
        except DuplicateKeyError:
            raise DuplicateEntity("file")
        except WriteError:
            raise UnableToCreate("request")

    @staticmethod
    async def generate_insights(data: dict, file_id: str, isAuth: bool):
        try:
            # get insights from intel API (mock)
            insight_id = IntelMockService.get_insight_id(data)
            if not insight_id:
                raise UnableToGet("insights")
            insights = await IntelMockService.get_insights(data, insight_id)
            if not insights:
                raise UnableToGet("insights")

            result = InsightAnalysis.analyze_insights(insights)
            if not result:
                raise UnableToCreate("insights")

            return result
        except WriteError:
            raise UnableToCreate("insights")

    @staticmethod
    async def get_insights_by_user_id(user_id: str):
        try:
            response = await RequestService.get_insights_by_user_id(user_id)
            if not response:
                raise EntityNotFound("Insights")
            return response
        except Exception:
            raise EntityNotFound("Insights list")
