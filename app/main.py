from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.db import get_db_without_generator, engine
from app.users.routes import router as users_router
from app.sales.routes import router as sales_router

async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    print("on")
    yield
    print("off")

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(sales_router)