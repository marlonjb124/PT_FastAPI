# Proyecto TODO API con FastAPI y PostgreSQL

Este proyecto implementa una API RESTful para la gestión de tareas (TODOs) multiusuario, siguiendo buenas prácticas de arquitectura y seguridad. Incluye autenticación JWT, PostgreSQL, SQLAlchemy asíncrono, migraciones con Alembic, Rate Limiting, Error Handler, Logging y despliegue con Docker.

## 🚀 Instrucciones para ejecutar el proyecto

### Prerrequisitos
- Docker y Docker Compose instalados
- Git (para clonar el repositorio)

### Pasos para ejecutar

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/marlonjb124/PT_FastAPI.git
   cd PTecnica_FastAPI
   ```

2. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env en la raíz del proyecto
   cp .env.example .env
   ```
   
   O crear manualmente el archivo `.env` con:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/todoapp
   SECRET_KEY=tu-clave-secreta-muy-segura
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. **Construir y ejecutar con Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Verificar que la aplicación esté funcionando**
   - API: http://localhost:8000
   - Documentación interactiva: http://localhost:8000/docs
   - Documentación alternativa: http://localhost:8000/redoc

### 📋 Probar la API

**Opción 1: Usar la documentación interactiva**
- Ir a http://localhost:8000/docs
- Probar endpoints directamente desde el navegador

**Opción 2: Importar en cliente HTTP (Postman, Insomnia, etc.)**
- Usar el archivo `PT.openapi.json` incluido en el proyecto
- Importar en tu cliente HTTP favorito
- Todos los endpoints y esquemas estarán configurados automáticamente(Editar los parametros de ser necesario)

### Comandos útiles

**Levantar los servicios:** 
```bash
docker-compose up --build
```



**Ejecutar migraciones manualmente:**
```bash
alembic upgrade head
```

SI SE DESEA DETENER LOS SERVICIOS
**Parar los servicios:**
```bash
docker-compose down
```

Si SE DESEA HACER SIN DOCKER
### Desarrollo local (sin Docker)

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar base de datos PostgreSQL local**
   - Instalar PostgreSQL
   - Crear base de datos `todoapp`
   - Actualizar `DATABASE_URL` en `.env`

4. **Ejecutar migraciones**
   ```bash
   alembic upgrade head
   ```

5. **Ejecutar la aplicación**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

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

- Dockerfile
- docker-compose.yml
- requirements.txt
- README.md

La creación de carpetas y archivos se realizará en los siguientes pasos.
