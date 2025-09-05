from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.auth import signupRequest, signupResponse, TokenResponse, LoginRequest
from app.models.user import User
from app.db.session import get_db
from app.core.security import JWTHandler
from app.core.logging import logger
from app.core.rate_limiting import limiter

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    logger.info(f"Login attempt for user: {form_data.username}")
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not JWTHandler.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    logger.info(f"User {form_data.username} logged in successfully")
    access_token = JWTHandler.create_access_token({"sub": user.username})
    return TokenResponse(access_token=access_token, expires_in=3600, token_type="bearer")

@router.post("/sign_up", response_model=signupResponse)
@limiter.limit("3/minute")
async def sign_up(http_request: Request, request: signupRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Signup attempt for username: {request.username}")
    # Check username
    result = await db.execute(select(User).where(User.username == request.username))
    user = result.scalar_one_or_none()
    if user:
        logger.warning(f"Signup failed: username {request.username} already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    # Check email
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    if user:
        logger.warning(f"Signup failed: email {request.email} already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user = User(username=request.username, email=request.email, hashed_password=JWTHandler.get_password_hash(request.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.info(f"User {new_user.username} created successfully with id {new_user.id}")
    return signupResponse(message="User created successfully")
    
    