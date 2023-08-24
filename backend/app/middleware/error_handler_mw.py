from fastapi import Request
from fastapi.responses import JSONResponse
import logging


async def exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred"},
        )
