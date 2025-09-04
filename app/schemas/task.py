from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.enums import TaskStatus

class TaskBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200, description="Task title")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Task description")
    estado: TaskStatus = Field(default=TaskStatus.PENDIENTE, description="Task status")

class TaskCreate(TaskBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "titulo": "Complete project documentation",
                "descripcion": "Write comprehensive API documentation",
                "estado": "pendiente"
            }
        }
    }

class TaskUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=1000)
    estado: Optional[TaskStatus] = None
    @field_validator('titulo')
    @classmethod
    def validate_titulo(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else v

class TaskResponse(TaskBase):
    id: UUID = Field(..., description="Task unique identifier")
    fecha_creacion: datetime = Field(..., description="Task creation timestamp")
    fecha_actualizacion: Optional[datetime] = Field(None, description="Last update timestamp")
    id_usuario: UUID = Field(..., description="Owner user ID")
    model_config = {
        "from_attributes": True
    }

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    limit: int = Field(..., description="Maximum number of tasks returned")
    offset: int = Field(..., description="Number of tasks skipped")

class TaskFilters(BaseModel):
    limit: int = Field(default=100, ge=1, le=1000, description="Items per page")
    offset: int = Field(default=0, ge=0, description="Number of items to skip")
    estado: Optional[TaskStatus] = Field(None, description="Filter by task status")
    search: Optional[str] = Field(None, max_length=100, description="Search in title and description")
    sort_by: Optional[str] = Field(default="fecha_creacion", pattern="^(fecha_creacion|titulo|estado)$")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")

class DeleteResponse(BaseModel):
    message: str = Field(..., description="Deletion confirmation message")
    deleted_at: datetime = Field(..., description="Deletion timestamp")
