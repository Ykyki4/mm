from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.sales import orm
from app.core.db import get_db
from app.sales.schemas import SaleCreate, SaleUpdate

router = APIRouter(prefix="/sales")


@router.get("")
async def get_sales(db: AsyncSession = Depends(get_db)):
    return await orm.get_sales(db)


@router.get("/{id}")
async def get_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    sale = await orm.get_sale(sale_id, db)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.post("")
async def create_sale(sale: SaleCreate, db: AsyncSession = Depends(get_db)):
    return await orm.create_sale(sale, db)


@router.patch("/{id}")
async def update_sale(sale_id: int, sale: SaleUpdate, db: AsyncSession = Depends(get_db)):
    db_sale = await orm.update_sale(sale_id, sale, db)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale


@router.delete("/{id}")
async def delete_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    success = await orm.delete_sale(sale_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
    return
