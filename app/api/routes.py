from fastapi import APIRouter
from . import dependencies
from fastapi import APIRouter
from app.api.auth_router import router as auth_router
from app.api.tasks_router import router as tasks_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
