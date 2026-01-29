from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.sales import orm
from app.core.db import get_db

router = APIRouter(prefix="/sales")


@router.get("")
async def get_sales(db: AsyncSession = Depends(get_db)):
    return orm.get_sales(db)