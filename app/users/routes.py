from passlib import hash
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.users.orm import get_user, create_user, authorize_user
from app.users.schemas import RegisterUser, LoginUser

router = APIRouter(prefix="/users")


@router.post("/register", )
async def register_user(data: RegisterUser, session: AsyncSession = Depends(get_db)):
    user = await get_user(data.username, session)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    data.password = hash.bcrypt(data.password)
    user = create_user(data, session)
    return user


@router.get("/login")
async def login_user(data: LoginUser, session: AsyncSession = Depends(get_db)):
    user = await authorize_user(data.username, data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
