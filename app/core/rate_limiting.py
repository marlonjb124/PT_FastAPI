from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse

# Create limiter instance with in-memory storage
limiter = Limiter(
    key_func=get_remote_address
)

# Custom rate limit exceeded handler
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": f"Rate limit exceeded: {exc.detail}",
            "retry_after": 60
        }
    )
    response.headers["Retry-After"] = "60"
    return response

# Rate limiting decorators for different endpoint types
def auth_rate_limit():
    """Rate limit for authentication endpoints - more restrictive"""
    return limiter.limit("5/minute")

def api_rate_limit():
    """Rate limit for general API endpoints"""
    return limiter.limit("60/minute")

def strict_rate_limit():
    """Rate limit for sensitive operations"""
    return limiter.limit("10/minute")
