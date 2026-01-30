from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

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

async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


def get_db_without_generator():
    db = async_session_factory()
    return db


async def get_db() -> Generator[AsyncSession, None, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
