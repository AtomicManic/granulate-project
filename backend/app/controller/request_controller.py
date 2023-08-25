from fastapi import Request, HTTPException, status
from typing import Dict
from jose import jwt, JWTError
from typing import Optional
import pymongo

from app.services.intel_mock_service import IntelMockService
from app.services.request_service import InsightRequest, TempRequest
from app.services.config import settings
from app.services.request_service import RequestService
from app.util.insights_analysis import InsightAnalysis
from app.models.request_model import InsightRequest


class RequestController:

    @staticmethod
    async def get_temp_request(request: Request):
        try:
            # Get cookie and decode
            cookie = request.cookies['anonymous_id']
            if cookie is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing Cookie"
                )
            user = jwt.decode(
                cookie, settings.JWT_SECRET_KEY, settings.ALGORITHM)
            user_id = user['user_id']
            suggestion = await RequestService.get_temp_by_id(user_id)
            return suggestion

        except JWTError as e:
            raise Exception(f"JWT decode Error:{e}")

        except pymongo.errors.WriteError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to save file to DB"
            )

        except Exception as e:
            raise Exception(e)

    @staticmethod
    async def save_temp_request(data: Dict, request: Request):
        try:
            # Get cookie and decode
            cookie = request.cookies.get("anonymous_id", None)
            if cookie is None:
                raise Exception("Cookie not found")
            user = jwt.decode(
                cookie, settings.JWT_SECRET_KEY, settings.ALGORITHM)
            # save suggestion
            new_data = await RequestService.save_temp_suggestion(data["data"], user_id=user['user_id'])
            return new_data

        except JWTError as e:
            raise Exception(f"JWT decode Error:{e}")

        except pymongo.errors.WriteError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to save file to DB"
            )

    @staticmethod
    async def save_auth_request(data: Dict, id: str):
        try:
            new_data = await RequestService.save_suggestion(data=data["data"], user_id=id)
            print('here2')
            return new_data
        except pymongo.errors.OperationFailure:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request."
            )

    @staticmethod
    async def generate_insights(data: dict, isAuth: bool, request: Request, id: Optional[str] = None):
        print("generate insights")
        try:
            # get insights from intel API (mock)
            insight_id = IntelMockService.get_insight_id(data)
            insights = await IntelMockService.get_insights(data, insight_id)

            result = InsightAnalysis.analyze_insights(insights)
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request."
            )


# 2023-08-25T09:44:33.440+00:00
