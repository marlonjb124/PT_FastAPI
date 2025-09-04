from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskFilters, DeleteResponse
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.task import Task
from app.db.session import get_db
from sqlalchemy.future import select
from app.core.logging import logger

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} creating a new task with title: {task.titulo}")
    new_task = Task(
        titulo=task.titulo,
        descripcion=task.descripcion,
        estado=task.estado,
        id_usuario=current_user.id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    logger.info(f"Task '{new_task.titulo}' created successfully for user {current_user.username} with id {new_task.id}")
    return TaskResponse.from_orm(new_task)

@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    result = await db.execute(select(Task).where(Task.id_usuario == current_user.id).offset(offset).limit(limit))
    tasks = result.scalars().all()
    total = len(tasks)
    return TaskListResponse(tasks=[TaskResponse.from_orm(t) for t in tasks], total=total, limit=limit, offset=offset)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} fetching task with id: {task_id}")
    result = await db.execute(select(Task).where(Task.id == task_id, Task.id_usuario == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning(f"User {current_user.username} failed to fetch task with id: {task_id}. Task not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"User {current_user.username} fetched task with id: {task_id} successfully.")
    return TaskResponse.from_orm(task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: UUID, updates: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} updating task with id: {task_id}")
    result = await db.execute(select(Task).where(Task.id == task_id, Task.id_usuario == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning(f"User {current_user.username} failed to update task with id: {task_id}. Task not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    logger.info(f"User {current_user.username} updated task with id: {task_id} successfully.")
    return TaskResponse.from_orm(task)

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
    from datetime import datetime
    logger.info(f"User {current_user.username} deleted task with id: {task_id} successfully.")
    return DeleteResponse(message="Task deleted", deleted_at=datetime.utcnow())
