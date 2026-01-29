from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

SERVER = '(localdb)\MSSQLLocalDB'
DATABASE = 'test'

import sqlalchemy as sa
connection_url_obj = sa.engine.URL.create(
    "mssql+aioodbc",
    host=SERVER,
    database=DATABASE,
    query={
        "Trusted_Connection": "yes",
        "driver": "ODBC Driver 17 for SQL Server"
    }
)

engine = create_async_engine(connection_url_obj)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_without_generator():
    db = SessionLocal()
    return db


def get_db() -> Generator[AsyncSession, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
