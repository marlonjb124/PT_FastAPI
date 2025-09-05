from fastapi import FastAPI, Request
import time

from app.api.routes import router as api_router
from app.core.logging import logger
from app.core.rate_limiting import limiter, rate_limit_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="TODO API", version="1.0.0")

# Add rate limiting state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url.path} - Completed in {process_time:.4f}s - Status: {response.status_code}")
    return response

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

app.include_router(api_router)
