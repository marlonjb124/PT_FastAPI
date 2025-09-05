from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from datetime import datetime,timezone
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskFilters, DeleteResponse
from app.models.task import Task
from app.models.user import User
from app.db.session import get_db
from app.api.dependencies import get_current_user
from sqlalchemy.future import select
from app.core.logging import logger
from app.core.rate_limiting import limiter

router = APIRouter()

@router.post("/", response_model=TaskResponse)
@limiter.limit("2/minute")
async def create_task(request: Request, task: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} creating a new task with title: {task.titulo}")
    result = await db.execute(select(Task).where(Task.titulo == task.titulo, Task.id_usuario == current_user.id))
    db_task = result.scalar_one_or_none()
    if db_task:
        logger.warning(f"User {current_user.username} failed to create task with title: {task.titulo}. Task already exists.")
        raise HTTPException(status_code=400, detail="Task already exists")
    new_task = Task(**task.model_dump(), id_usuario=current_user.id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    logger.info(f"Task '{new_task.titulo}' created successfully for user {current_user.username} with id {new_task.id}")
    return TaskResponse.model_validate(new_task)

@router.get("/", response_model=TaskListResponse)
@limiter.limit("60/minute")
async def list_tasks(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    result = await db.execute(select(Task).where(Task.id_usuario == current_user.id).offset(offset).limit(limit))
    tasks = result.scalars().all()
    total = len(tasks)
    return TaskListResponse(tasks=[TaskResponse.model_validate(t) for t in tasks], total=total, limit=limit, offset=offset)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} fetching task with id: {task_id}")
    result = await db.execute(select(Task).where(Task.id == task_id, Task.id_usuario == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning(f"User {current_user.username} failed to fetch task with id: {task_id}. Task not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"User {current_user.username} fetched task with id: {task_id} successfully.")
    return TaskResponse.model_validate(task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: UUID, updates: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} updating task with id: {task_id}")
    result = await db.execute(select(Task).where(Task.id == task_id, Task.id_usuario == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning(f"User {current_user.username} failed to update task with id: {task_id}. Task not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    logger.info(f"User {current_user.username} updated task with id: {task_id} successfully.")
    return TaskResponse.model_validate(task)

@router.delete("/{task_id}", response_model=DeleteResponse)
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} deleting task with id: {task_id}")
    result = await db.execute(select(Task).where(Task.id == task_id, Task.id_usuario == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning(f"User {current_user.username} failed to delete task with id: {task_id}. Task not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()

    logger.info(f"User {current_user.username} deleted task with id: {task_id} successfully.")
    return DeleteResponse(message="Task deleted", deleted_at=datetime.now(timezone.utc))
