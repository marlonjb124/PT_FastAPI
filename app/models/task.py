from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import TaskStatus

class Task(Base):
    __tablename__ = "tasks"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Enum(TaskStatus), default=TaskStatus.PENDIENTE)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow)
    id_usuario = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")
    __table_args__ = (
        Index("idx_tasks_user_id", "id_usuario"),
        Index("idx_tasks_estado", "estado"),
        Index("idx_tasks_fecha_creacion", "fecha_creacion"),
    )
