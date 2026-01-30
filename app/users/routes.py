from passlib.hash import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.core.db import get_db
from app.users.orm import get_user, create_user, authorize_user
from app.users.schemas import RegisterUser, LoginUser, UserResponse

router = APIRouter(prefix="/users")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/register", response_model=UserResponse)
async def register_user(data: RegisterUser, session: AsyncSession = Depends(get_db)):
    user = await get_user(data.username, session)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    data.password = pwd_context.hash(data.password)
    user = await create_user(data, session)
    return user


@router.post("/login", response_model=UserResponse)
async def login_user(data: LoginUser, session: AsyncSession = Depends(get_db)):
    user = await get_user(data.username, session)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=404, detail="User does not exist")
    return user
