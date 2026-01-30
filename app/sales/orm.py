from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Sale
from app.sales.schemas import SaleCreate, SaleUpdate


async def get_sales(db: AsyncSession):
    query = select(Sale)
    sales = (await db.execute(query)).scalars().all()
    return sales


async def get_sale(sale_id: int, db: AsyncSession):
    sale = await db.get(Sale, sale_id)
    return sale


async def create_sale(sale: SaleCreate, db: AsyncSession):
    sale = Sale(**sale.model_dump())
    db.add(sale)
    await db.commit()
    return sale


async def update_sale(sale_id: int, sale: SaleUpdate, db: AsyncSession):
    db_sale = await db.get(Sale, sale_id)
    if not db_sale:
        return None
    db_sale.sqlmodel_update(sale)
    db.add(db_sale)
    await db.commit()
    return db_sale


async def delete_sale(sale_id: int, db: AsyncSession):
    db_sale = await db.get(Sale, sale_id)
    if not db_sale:
        return False
    await db.delete(db_sale)
    await db.commit()
    return True
