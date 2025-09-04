from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import JWTHandler
from app.models.user import User
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = JWTHandler.decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    username: str = payload["sub"]
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
