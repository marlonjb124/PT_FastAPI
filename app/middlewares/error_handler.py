from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("uvicorn.error")

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Unhandled error: {exc}")
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
