from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.users.schemas import RegisterUser


async def create_user(data: RegisterUser, db: AsyncSession):
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    return user


async def get_user(username: str, db: AsyncSession) -> User | None:
    query = select(User).where(User.username == username)
    user = (await db.execute(query)).scalars().one_or_none()
    return user


async def authorize_user(username: str, password: str, db: AsyncSession) -> User | None:
    query = select(User).where(User.username == username, User.password == password)