# Proyecto TODO API con FastAPI y PostgreSQL

Este proyecto implementa una API RESTful para la gestión de tareas (TODOs) multiusuario, siguiendo las mejores prácticas de arquitectura y seguridad. Incluye autenticación JWT, PostgreSQL, SQLAlchemy asíncrono, migraciones con Alembic, y despliegue con Docker.

## Estructura propuesta

- app/
  - main.py
  - api/
    - __init__.py
    - routes.py
    - dependencies.py
  - core/
    - __init__.py
    - config.py
    - security.py
  - models/
    - __init__.py
    - user.py
    - task.py
    - enums.py
  - schemas/
    - __init__.py
    - auth.py
    - task.py
  - services/
    - __init__.py
    - task_service.py
    - user_service.py
  - repository/
    - __init__.py
    - task_repository.py
    - user_repository.py
  - db/
    - __init__.py
    - session.py
    - base.py
  - middlewares/
    - __init__.py
    - auth.py
    - error_handler.py
    - logging.py
    - rate_limit.py
- alembic/
- tests/
- Dockerfile
- docker-compose.yml
- requirements.txt
- README.md

La creación de carpetas y archivos se realizará en los siguientes pasos.
