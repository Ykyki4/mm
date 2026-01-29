from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Sale


async def get_sales(db: AsyncSession):
    query = select(Sale)
    sales = (await db.execute(query)).scalars().all()
    return sales