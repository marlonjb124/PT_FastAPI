from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import JWTHandler

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/auth/") or request.url.path == "/openapi.json":
            return await call_next(request)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
        token = auth_header.split(" ")[1]
        payload = JWTHandler.decode_access_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        request.state.user = payload.get("sub")
        return await call_next(request)
