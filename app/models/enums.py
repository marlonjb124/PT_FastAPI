from enum import Enum

class TaskStatus(str, Enum):
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
